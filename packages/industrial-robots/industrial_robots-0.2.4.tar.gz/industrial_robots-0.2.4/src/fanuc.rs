use industrial_robots::Point3;
use crate::mesh::mesh_to_numpy;
use crate::utility::Frame3;
use numpy::ndarray::ArrayD;
use numpy::{IntoPyArray, PyArrayDyn, PyUntypedArrayMethods};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

enum CrxType {
    Crx5ia,
    Crx10ia,
}

#[pyclass]
pub struct Crx {
    inner: industrial_robots::fanuc::Crx,
    crx_type: CrxType,
}

impl Crx {
    pub fn get_inner(&self) -> &industrial_robots::fanuc::Crx {
        &self.inner
    }
}

#[pymethods]
impl Crx {
    fn get_meshes<'py>(
        &self,
        py: Python<'py>,
    ) -> PyResult<Vec<(Bound<'py, PyArrayDyn<f64>>, Bound<'py, PyArrayDyn<u32>>)>> {
        let mut result = Vec::new();
        let meshes = match self.crx_type {
            CrxType::Crx5ia => Ok(industrial_robots::fanuc::crx5ia_mesh()),
            CrxType::Crx10ia => Ok(industrial_robots::fanuc::crx10ia_mesh()),
            _ => Err(PyValueError::new_err("Unknown CRX type")),
        }?;

        for (vertices, faces) in meshes {
            result.push(mesh_to_numpy(py, vertices, faces)?);
        }

        Ok(result)
    }

    #[staticmethod]
    fn new_5ia() -> Self {
        Self {
            inner: industrial_robots::fanuc::Crx::new_5ia(),
            crx_type: CrxType::Crx5ia,
        }
    }

    #[staticmethod]
    fn new_10ia() -> Self {
        Self {
            inner: industrial_robots::fanuc::Crx::new_10ia(),
            crx_type: CrxType::Crx10ia,
        }
    }
    
    fn ik(&self, target: &Frame3) -> Vec<Vec<f64>> {
        // let start = std::time::Instant::now();
        let ik_solutions = self.inner.ik(target.get_inner());
        // let duration = start.elapsed();
        // println!("IK time: {:?}", duration);

        ik_solutions.iter().map(|j| j.to_vec()).collect()
    }
    
    fn brute_force(&self, target: &Frame3) -> (Vec<f64>, Vec<f64>) {
        let start = std::time::Instant::now();
        let (upper, lower) = self.inner.brute_force_o3(target.get_inner());
        let duration = start.elapsed();
        println!("Brute force time: {:?}", duration);

        (upper, lower)
    }

    fn error<'py>(&self, py: Python<'py>, n: usize, target: &Frame3) -> Bound<'py, PyArrayDyn<f64>> {
        let o5 = target.get_inner() * Point3::new(0.0, 0.0, -self.inner.x2());

        let mut values = Vec::with_capacity(n);
        let step = 2.0 / n as f64;
        
        // Time this loop
        let start = std::time::Instant::now();

        for i in 0..n {
            let theta = i as f64 * step * std::f64::consts::PI;
            values.push(self.inner.error(theta, target.get_inner(), &o5));
        }
        
        // Print the time taken
        let duration = start.elapsed();
        println!("Time taken: {:?}", duration);

        let mut result = ArrayD::zeros(vec![values.len(), 3]);
        for (i, (u, l)) in values.iter().enumerate() {
            result[[i, 0]] = i as f64 * step * std::f64::consts::PI;
            result[[i, 1]] = *u;
            result[[i, 2]] = *l;
        }

        result.into_pyarray(py)
    }

    fn o4_circle<'py>(&self, py: Python<'py>, end_frame: &Frame3) -> Bound<'py, PyArrayDyn<f64>> {
        let points = self.inner.o4_circle(end_frame.get_inner());

        let mut result = ArrayD::zeros(vec![points.len(), 3]);
        for (i, point) in points.iter().enumerate() {
            result[[i, 0]] = point.x;
            result[[i, 1]] = point.y;
            result[[i, 2]] = point.z;
        }

        result.into_pyarray(py)
    }

    fn o3_points<'py>(
        &self,
        py: Python<'py>,
        end_frame: &Frame3,
    ) -> (Bound<'py, PyArrayDyn<f64>>, Bound<'py, PyArrayDyn<f64>>) {
        let (uppers, lowers) = self.inner.o3_points(end_frame.get_inner());

        let mut upper_result = ArrayD::zeros(vec![uppers.len(), 3]);
        let mut lower_result = ArrayD::zeros(vec![lowers.len(), 3]);

        for (i, point) in uppers.iter().enumerate() {
            upper_result[[i, 0]] = point.x;
            upper_result[[i, 1]] = point.y;
            upper_result[[i, 2]] = point.z;
        }

        for (i, point) in lowers.iter().enumerate() {
            lower_result[[i, 0]] = point.x;
            lower_result[[i, 1]] = point.y;
            lower_result[[i, 2]] = point.z;
        }

        (upper_result.into_pyarray(py), lower_result.into_pyarray(py))
    }

    // fn ik(&self, frame: &Frame3) {
    //     self.inner.ik(&frame.get_inner())
    // }

    fn fk(&self, joints: Vec<f64>) -> PyResult<Frame3> {
        if joints.len() != 6 {
            return Err(PyValueError::new_err("Expected 6 joint angles"));
        }
        let joints: [f64; 6] = [
            joints[0], joints[1], joints[2], joints[3], joints[4], joints[5],
        ];
        let frame = self.inner.fk(&joints);
        Ok(Frame3::from_inner(frame))
    }

    fn fk_all(&self, joints: Vec<f64>) -> PyResult<Vec<Frame3>> {
        if joints.len() != 6 {
            return Err(PyValueError::new_err("Expected 6 joint angles"));
        }
        let joints: [f64; 6] = [
            joints[0], joints[1], joints[2], joints[3], joints[4], joints[5],
        ];
        let results = self.inner.fk_all(&joints);

        // Convert the results to a Vec<Frame3>
        Ok(results.map(|f| Frame3::from_inner(f)).to_vec())
    }

    #[getter]
    fn z0(&self) -> f64 {
        self.inner.z0()
    }

    #[getter]
    fn z1(&self) -> f64 {
        self.inner.z1()
    }

    #[getter]
    fn x1(&self) -> f64 {
        self.inner.x1()
    }

    #[getter]
    fn x2(&self) -> f64 {
        self.inner.x2()
    }

    #[getter]
    fn y1(&self) -> f64 {
        self.inner.y1()
    }
}
