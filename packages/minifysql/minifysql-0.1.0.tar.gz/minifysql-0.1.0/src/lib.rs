use pyo3::prelude::*;
use sql_minifier::minify_sql;

#[pyfunction]
fn minify(sql: &str) -> PyResult<String> {
    if sql.is_empty() {
        Err(pyo3::exceptions::PyValueError::new_err("Input string cannot be empty"))
    } else {
        let minified: String = minify_sql(sql);
        Ok(minified)
    }
}

#[pymodule]
fn minifysql(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(minify, m)?)?;
    Ok(())
}
