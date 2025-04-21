use industrial_robots::{Point3, TriMesh, Vector3};
use numpy::ndarray::ArrayView2;
use numpy::PyReadonlyArray2;
use pyo3::exceptions::PyValueError;
use pyo3::PyResult;

pub fn array_to_faces(array: &ArrayView2<'_, u32>) -> PyResult<Vec<[u32; 3]>> {
    let shape = array.shape();
    if shape.len() != 2 || shape[1] != 3 {
        return Err(PyValueError::new_err("Expected Nx3 array of faces"));
    }

    Ok(array
        .rows()
        .into_iter()
        .map(|row| [row[0], row[1], row[2]])
        .collect())
}

pub fn array_to_points3(array: &ArrayView2<'_, f64>) -> PyResult<Vec<Point3>> {
    let shape = array.shape();
    if shape.len() != 2 || shape[1] != 3 {
        return Err(PyValueError::new_err("Expected Nx3 array of faces"));
    }

    Ok(array
        .rows()
        .into_iter()
        .map(|row| Point3::new(row[0], row[1], row[2]))
        .collect())
}

pub fn array_to_vectors3(array: &ArrayView2<'_, f64>) -> PyResult<Vec<Vector3>> {

    let shape = array.shape();
    if shape.len() != 2 || shape[1] != 3 {
        return Err(PyValueError::new_err("Expected Nx3 array of faces"));
    }

    Ok(array
        .rows()
        .into_iter()
        .map(|row| Vector3::new(row[0], row[1], row[2]))
        .collect())
}

pub fn to_tri_mesh<'py>(
    vertices: PyReadonlyArray2<'py, f64>,
    faces : PyReadonlyArray2<'py, u32>,
) -> PyResult<TriMesh> {
    let vertices = array_to_points3(&vertices.as_array())?;
    let faces = array_to_faces(&faces.as_array())?;
    let mesh = TriMesh::new(vertices, faces)
        .map_err(|e| PyValueError::new_err(e.to_string()))?;

    Ok(mesh)
}