//! Micro mesh format, used to store meshes in internal binary data.  Works for meshes that have
//! less than u16::MAX vertices, and discretizes the positions to 1/u16::MAX increments in an
//! axis-aligned bounding box of a size specified.
use crate::{Point3, Result};

fn aabb(points: &[Point3]) -> (Point3, Point3) {
    let mut min = Point3::new(f64::MAX, f64::MAX, f64::MAX);
    let mut max = Point3::new(f64::MIN, f64::MIN, f64::MIN);

    for point in points {
        min.x = min.x.min(point.x);
        min.y = min.y.min(point.y);
        min.z = min.z.min(point.z);
        max.x = max.x.max(point.x);
        max.y = max.y.max(point.y);
        max.z = max.z.max(point.z);
    }

    (min, max)
}

fn to_u16(value: f64, min: f64, max: f64) -> u16 {
    let range = max - min;
    let scale = u16::MAX as f64 / range;
    ((value - min) * scale).round() as u16
}

struct ByteRead<'a> {
    bytes: &'a [u8],
    offset: usize,
}

impl<'a> ByteRead<'a> {
    fn new(bytes: &'a [u8]) -> Self {
        ByteRead { bytes, offset: 0 }
    }

    fn read_f64(&mut self) -> f64 {
        let value =
            f64::from_le_bytes(self.bytes[self.offset..self.offset + 8].try_into().unwrap());
        self.offset += 8;
        value
    }

    fn read_u16(&mut self) -> u16 {
        let value =
            u16::from_le_bytes(self.bytes[self.offset..self.offset + 2].try_into().unwrap());
        self.offset += 2;
        value
    }

    fn read_u32(&mut self) -> u32 {
        let value =
            u32::from_le_bytes(self.bytes[self.offset..self.offset + 4].try_into().unwrap());
        self.offset += 4;
        value
    }
}

pub fn bytes_to_mesh(bytes: &[u8]) -> Result<(Vec<Point3>, Vec<[u32; 3]>)> {
    let mut reader = ByteRead::new(bytes);

    // Read the bounding box
    let min = Point3::new(reader.read_f64(), reader.read_f64(), reader.read_f64());
    let max = Point3::new(reader.read_f64(), reader.read_f64(), reader.read_f64());

    // Read the number of vertices
    let vertex_count = reader.read_u16() as usize;

    // Read the vertices
    let mut vertices = Vec::with_capacity(vertex_count);
    for _ in 0..vertex_count {
        let x = min.x
            + (f64::from(reader.read_u16()) / u16::MAX as f64) * (max.x - min.x);
        let y = min.y
            + (f64::from(reader.read_u16()) / u16::MAX as f64) * (max.y - min.y);
        let z = min.z
            + (f64::from(reader.read_u16()) / u16::MAX as f64) * (max.z - min.z);
        vertices.push(Point3::new(x, y, z));
    }

    // Read the number of triangles
    let triangle_count = reader.read_u32() as usize;

    // Read the triangles
    let mut triangles = Vec::with_capacity(triangle_count);

    for _ in 0..triangle_count {
        triangles.push([
            reader.read_u16() as u32,
            reader.read_u16() as u32,
            reader.read_u16() as u32,
        ]);
    }

    Ok((vertices, triangles))
}

pub fn mesh_to_bytes(vertices: &[Point3], triangles: &[[u32; 3]]) -> Result<Vec<u8>> {
    // Check if the number of vertices is less than u16::MAX
    if vertices.len() > u16::MAX as usize {
        return Err("Mesh has too many vertices for the small format".into());
    }

    let mut output = Vec::new();

    // Get the AABB of the mesh
    let (min, max) = aabb(vertices);
    output.extend_from_slice(&min.x.to_le_bytes());
    output.extend_from_slice(&min.y.to_le_bytes());
    output.extend_from_slice(&min.z.to_le_bytes());
    output.extend_from_slice(&max.x.to_le_bytes());
    output.extend_from_slice(&max.y.to_le_bytes());
    output.extend_from_slice(&max.z.to_le_bytes());

    // Write the number of vertices
    output.extend_from_slice(&(vertices.len() as u16).to_le_bytes());

    // Write the vertices
    for p in vertices {
        output.extend_from_slice(&to_u16(p.x, min.x, max.x).to_le_bytes());
        output.extend_from_slice(&to_u16(p.y, min.y, max.y).to_le_bytes());
        output.extend_from_slice(&to_u16(p.z, min.z, max.z).to_le_bytes());
    }

    // Write the number of triangles
    output.extend_from_slice(&(triangles.len() as u32).to_le_bytes());

    // Write the triangles
    for triangle in triangles {
        output.extend_from_slice(&(triangle[0] as u16).to_le_bytes());
        output.extend_from_slice(&(triangle[1] as u16).to_le_bytes());
        output.extend_from_slice(&(triangle[2] as u16).to_le_bytes());
    }

    Ok(output)
}
