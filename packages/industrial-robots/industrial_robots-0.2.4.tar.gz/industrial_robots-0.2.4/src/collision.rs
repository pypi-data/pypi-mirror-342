use crate::helpers::to_tri_mesh;
use crate::utility::Frame3;
use industrial_robots as ir;
use numpy::PyReadonlyArray2;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

#[pyclass]
pub struct CollisionScene {
    inner: ir::CollisionScene,
}

impl CollisionScene {
    pub fn get_inner(&self) -> &ir::CollisionScene {
        &self.inner
    }

    pub fn from_inner(inner: ir::CollisionScene) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl CollisionScene {
    #[new]
    fn new() -> Self {
        Self {
            inner: ir::CollisionScene::new(),
        }
    }

    fn __repr__(&self) -> String {
        format!("<CollisionScene with {} meshes>", self.inner.len())
    }

    fn __len__(&self) -> usize {
        self.inner.len()
    }

    fn add_background<'py>(
        &mut self,
        vertices: PyReadonlyArray2<'py, f64>,
        faces : PyReadonlyArray2<'py, u32>,
    ) -> PyResult<usize> {
        let mesh = to_tri_mesh(vertices, faces)?;
        Ok(self.inner.add_background(mesh))
    }

    fn add_interest<'py>(
        &mut self,
        vertices: PyReadonlyArray2<'py, f64>,
        faces : PyReadonlyArray2<'py, u32>,
    ) -> PyResult<usize> {
        let mesh = to_tri_mesh(vertices, faces)?;
        Ok(self.inner.add_interest(mesh))
    }

    fn remove_mesh(&mut self, id: usize) {
        self.inner.remove_mesh(id);
    }

    fn add_exclusion(&mut self, id1: usize, id2: usize) {
        self.inner.add_exclusion(id1, id2);
    }

    fn remove_exclusion(&mut self, id1: usize, id2: usize) {
        self.inner.remove_exclusion(id1, id2);
    }

    #[pyo3(signature=(transforms, stop_at_first=false, skip_ids=None))]
    fn check_all(
        &self,
        transforms: Vec<(usize, Frame3)>,
        stop_at_first: bool,
        skip_ids: Option<Vec<usize>>
    ) -> PyResult<Vec<(usize, usize)>> {
        let transforms = transforms
            .into_iter()
            .map(|(id, frame)| (id, frame.get_inner().clone()))
            .collect::<Vec<_>>();

        let skip_ids = skip_ids.as_ref().map(Vec::as_slice);

        let result = self.inner.check_all(&transforms, stop_at_first, skip_ids)
            .map_err(|e| PyValueError::new_err(format!("Collision check failed: {}", e)))?;

        Ok(result)
    }

    fn distances(
        &self,
        id1: usize,
        id2: Vec<usize>,
        transforms: Vec<(usize, Frame3)>,
    ) -> PyResult<Vec<f64>> {
        let transforms = transforms
            .into_iter()
            .map(|(id, frame)| (id, frame.get_inner().clone()))
            .collect::<Vec<_>>();

        let result = self.inner.distances(id1, &id2, &transforms)
            .map_err(|e| PyValueError::new_err(format!("Distance check failed: {}", e)))?;

        Ok(result)
    }


}

