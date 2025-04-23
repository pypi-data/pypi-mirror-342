use pyo3::prelude::*;

mod filedb;
mod fsdb;
mod nil;
mod pydb;
mod ram;

pub fn populate_module(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(nil::hash, m)?)?;
    m.add_class::<fsdb::FsDB>()?;
    m.add_class::<filedb::FileDB>()?;
    m.add_class::<pydb::PyDB>()?;
    m.add_class::<ram::Ram>()?;
    Ok(())
}
