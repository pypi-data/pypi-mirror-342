use pyo3::prelude::*;

mod fanuc;
mod mesh;
mod utility;
mod collision;
mod helpers;

fn register_fanuc_module(parent_module: &Bound<'_, PyModule>) -> PyResult<()> {
    let child = PyModule::new(parent_module.py(), "_fanuc")?;
    child.add_class::<fanuc::Crx>()?;

    parent_module.add_submodule(&child)
}

#[pymodule(name = "industrial_robots")]
fn py_industrial_robots(m: &Bound<'_, PyModule>) -> PyResult<()> {
    register_fanuc_module(m)?;

    m.add_class::<utility::Frame3>()?;
    m.add_class::<collision::CollisionScene>()?;

    m.add_function(wrap_pyfunction!(mesh::micro_serialize, m)?)?;
    m.add_function(wrap_pyfunction!(mesh::micro_deserialize, m)?)?;

    Ok(())
}
