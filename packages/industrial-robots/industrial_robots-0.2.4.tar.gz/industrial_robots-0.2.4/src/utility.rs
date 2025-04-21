use crate::helpers::{array_to_points3, array_to_vectors3};
use industrial_robots::nalgebra::{try_convert, Matrix4};
use numpy::ndarray::ArrayD;
use numpy::{IntoPyArray, PyArrayDyn, PyReadonlyArray2, PyReadonlyArrayDyn, PyUntypedArrayMethods};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

#[pyclass]
#[derive(Debug, Clone)]
pub struct Frame3 {
    inner: industrial_robots::Frame3,
}

impl Frame3 {
    pub fn from_inner(inner: industrial_robots::Frame3) -> Self {
        Self { inner }
    }

    pub fn get_inner(&self) -> &industrial_robots::Frame3 {
        &self.inner
    }
}

#[pymethods]
impl Frame3 {
    fn __repr__(&self) -> String {
        format!(
            "<Frame3 t=[{}, {}, {}] r=[{}, {}, {}, {}]>",
            self.inner.translation.x,
            self.inner.translation.y,
            self.inner.translation.z,
            self.inner.rotation.i,
            self.inner.rotation.j,
            self.inner.rotation.k,
            self.inner.rotation.w,
        )
    }

    #[getter]
    fn origin(&self) -> (f64, f64, f64) {
        (
            self.inner.translation.x,
            self.inner.translation.y,
            self.inner.translation.z,
        )
    }

    #[staticmethod]
    fn from_xyzwpr(x: f64, y: f64, z: f64, w: f64, p: f64, r: f64) -> Self {
        Self {
            inner: industrial_robots::XyzWpr::new(x, y, z, w, p, r).to_isometry(),
        }
    }

    fn to_xyzwpr(&self) -> Vec<f64> {
        let v = industrial_robots::XyzWpr::from_isometry(&self.inner);
        vec![v.x, v.y, v.z, v.w, v.p, v.r]
    }

    #[new]
    fn new(matrix: PyReadonlyArrayDyn<'_, f64>) -> PyResult<Self> {
        if matrix.shape().len() != 2 || matrix.shape()[0] != 4 || matrix.shape()[1] != 4 {
            return Err(PyValueError::new_err("Expected 4x4 matrix"));
        }

        let mut array = [0.0; 16];
        for (i, value) in matrix.as_array().iter().enumerate() {
            array[i] = *value;
        }

        let inner = try_convert(Matrix4::from_row_slice(&array))
            .ok_or(PyValueError::new_err("Could not convert to isometry"))?;

        Ok(Self { inner })
    }

    #[staticmethod]
    fn from_translation(x: f64, y: f64, z: f64) -> Self {
        Self {
            inner: industrial_robots::Frame3::translation(x, y, z),
        }
    }

    #[staticmethod]
    fn from_rotation(angle: f64, a: f64, b: f64, c: f64) -> Self {
        let axis =
            industrial_robots::UnitVector3::new_normalize(industrial_robots::Vector3::new(a, b, c));
        let rot_vec = axis.into_inner() * angle;

        Self {
            inner: industrial_robots::Frame3::rotation(rot_vec),
        }
    }

    fn inverse(&self) -> Self {
        Self {
            inner: self.inner.inverse(),
        }
    }

    fn __matmul__(&self, other: &Frame3) -> PyResult<Self> {
        Ok(Frame3::from_inner(self.inner * other.inner))
    }

    fn as_numpy<'py>(&self, py: Python<'py>) -> Bound<'py, PyArrayDyn<f64>> {
        let mut result = ArrayD::zeros(vec![4, 4]);
        let m = self.inner.to_matrix();
        // TODO: In a rush, fix this later
        result[[0, 0]] = m.m11;
        result[[0, 1]] = m.m12;
        result[[0, 2]] = m.m13;
        result[[0, 3]] = m.m14;
        result[[1, 0]] = m.m21;
        result[[1, 1]] = m.m22;
        result[[1, 2]] = m.m23;
        result[[1, 3]] = m.m24;
        result[[2, 0]] = m.m31;
        result[[2, 1]] = m.m32;
        result[[2, 2]] = m.m33;
        result[[2, 3]] = m.m34;
        result[[3, 0]] = m.m41;
        result[[3, 1]] = m.m42;
        result[[3, 2]] = m.m43;
        result[[3, 3]] = m.m44;
        result.into_pyarray(py)
    }

    #[staticmethod]
    fn identity() -> Self {
        Self {
            inner: industrial_robots::Frame3::identity(),
        }
    }

    fn transform_points<'py>(
        &self,
        py: Python<'py>,
        points: PyReadonlyArray2<'py, f64>,
    ) -> PyResult<Bound<'py, PyArrayDyn<f64>>> {
        let points = array_to_points3(&points.as_array())?;
        let mut result = ArrayD::zeros(vec![points.len(), 3]);

        for (i, point) in points.iter().enumerate() {
            let transformed = self.inner * point;
            result[[i, 0]] = transformed.x;
            result[[i, 1]] = transformed.y;
            result[[i, 2]] = transformed.z;
        }

        Ok(result.into_pyarray(py))
    }

    fn transform_vectors<'py>(
        &self,
        py: Python<'py>,
        vectors: PyReadonlyArray2<'py, f64>,
    ) -> PyResult<Bound<'py, PyArrayDyn<f64>>> {
        let vectors = array_to_vectors3(&vectors.as_array())?;
        let mut result = ArrayD::zeros(vec![vectors.len(), 3]);

        for (i, vector) in vectors.iter().enumerate() {
            let transformed = self.inner * vector;
            result[[i, 0]] = transformed.x;
            result[[i, 1]] = transformed.y;
            result[[i, 2]] = transformed.z;
        }

        Ok(result.into_pyarray(py))
    }
}

#[cfg(test)]
mod tests {}
