use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyList;
use text2num::{
    get_interpreter_for, replace_numbers_in_text, text2digits, word_to_digit::find_numbers_iter,
    Occurence, Token,
};

/// Return the text of ``text`` with all the ``lang`` spelled numbers converted to digits.
///
/// The function is punctuation aware.
///
/// Isolated numbers, that is, integers and ordinals that don't belong to a group of numbers, are converted
/// if and only if their value is above the ``threshold``.
#[pyfunction]
#[pyo3(signature = (text, lang, threshold=3.0))]
fn alpha2digit(text: &str, lang: &str, threshold: f64) -> PyResult<String> {
    let interpreter = get_interpreter_for(lang)
        .ok_or_else(|| PyValueError::new_err(format!("unsupported language {lang}")))?;
    Ok(replace_numbers_in_text(text, &interpreter, threshold))
}

/// Convert the ``text`` string containing an integer number written as letters
///    into an integer value.
///
///    Raises a ValueError if ``text`` does not describe a valid number.
///    Return an int.
#[pyfunction]
#[pyo3(name = "text2num")]
fn text_to_num(text: &str, lang: &str) -> PyResult<i64> {
    let interpreter = get_interpreter_for(lang)
        .ok_or_else(|| PyValueError::new_err(format!("unsupported language {lang}")))?;
    text2digits(text, &interpreter)
        .map_err(|_| PyValueError::new_err(format!("invalid literal for text2num: '{text}'")))
        .and_then(|v| v.parse::<i64>().map_err(|e| e.into()))
}

struct TokenAdaptor<'a> {
    model: Bound<'a, PyAny>,
    text_cache: String,
    text_cache_lowercase: String,
}

impl<'a> TokenAdaptor<'a> {
    pub fn new(model: Bound<'a, PyAny>) -> Self {
        let py_result: Bound<'_, PyAny> = model.call_method0("text").unwrap();

        if py_result.get_type().name().unwrap() != "str" {
            panic!(
                "Expected a str for the get_results() method signature, got {}",
                py_result.get_type().name().unwrap()
            );
        }
        let text_cache: String = py_result.extract().unwrap();
        Self {
            model,
            text_cache_lowercase: text_cache.to_lowercase(),
            text_cache,
        }
    }
}

impl<'a> Token for TokenAdaptor<'a> {
    fn text(&self) -> &str {
        self.text_cache.as_str()
    }

    fn text_lowercase(&self) -> &str {
        &self.text_cache_lowercase.as_str()
    }

    fn nt_separated(&self, previous: &Self) -> bool {
        self.model
            .call_method1("nt_separated", (&previous.model,))
            .unwrap()
            .extract()
            .unwrap()
    }

    fn not_a_number_part(&self) -> bool {
        self.model.call_method0("not_a_number_part").unwrap().extract().unwrap()
    }
}

/// An occurence of a number was found in the sequence of tokens.
///
/// An occurence can span multiple consecutive tokens.
#[pyclass]
#[pyo3(name = "Occurence")]
pub struct NumOccurence {
    occurence: Occurence,
}

#[pymethods]
impl NumOccurence {
    /// Offset in the sequence of tokens where the number starts.
    #[getter]
    pub fn start(&self) -> usize {
        self.occurence.start
    }

    /// Offset in the sequence of tokens where the number ends.
    #[getter]
    pub fn end(&self) -> usize {
        self.occurence.end
    }

    /// The value of the number as float
    #[getter]
    pub fn value(&self) -> f64 {
        self.occurence.value
    }

    /// The text representation of the number.
    #[getter]
    pub fn text(&self) -> &str {
        self.occurence.text.as_str()
    }

    /// Is this an ordinal?
    #[getter]
    pub fn is_ordinal(&self) -> bool {
        self.occurence.is_ordinal
    }
}

/// Find the numbers and their positions in a stream of Tokens (the ``input``).
/// Return a list of ``Occurence`` instances.
#[pyfunction]
#[pyo3(signature = (input, lang, threshold=3.0))]
pub fn find_numbers(
    input: &Bound<'_, PyList>,
    lang: &str,
    threshold: f64,
) -> PyResult<Vec<NumOccurence>> {
    let interpreter = get_interpreter_for(lang)
        .ok_or_else(|| PyValueError::new_err(format!("unsupported language {lang}")))?;
    Ok(
        find_numbers_iter(input.iter().map(TokenAdaptor::new), &interpreter, threshold)
            .map(|o| NumOccurence { occurence: o })
            .collect(),
    )
}

/// Text2num
#[pymodule]
fn _text2num(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(alpha2digit, m)?)?;
    m.add_function(wrap_pyfunction!(text_to_num, m)?)?;
    m.add_function(wrap_pyfunction!(find_numbers, m)?)?;
    m.add_class::<NumOccurence>()?;
    Ok(())
}
