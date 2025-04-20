# Telugu Stopwords

A comprehensive Python library for Telugu stopwords, designed for natural language processing (NLP) tasks such as text preprocessing for hate speech detection, sentiment analysis, and topic modeling.

## Features

- Extensive list of Telugu stopwords in both Telugu script and English transliteration.
- Support for adding/removing custom stopwords.
- JSON save/load functionality for easy integration.
- Simple function to remove stopwords from text.
- Compatible with code-mixed Telugu-English text (e.g., social media).
- User-friendly imports with aliases: `tsw` for `TeluguStopWords` and `rmtsw` for `remove_stopwords`.
- Stopwords sorted to prioritize Telugu script for better readability.

## Installation

Install via pip:

```bash
pip install telugu-stopwords
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/PavanYellathakota/telugu-stopwords.git
```

For development, install locally in editable mode:

```bash
cd telugu-stopwords
pip install -e .
```

## Usage

```python
from telugu_stopwords import tsw, rmtsw

# Initialize
telugu_sw = tsw()

# Get stopwords
stopwords = telugu_sw.get_stopwords(script="telugu")
print(stopwords[:5])  # ['మరియు', 'లేదా', 'కానీ', 'అయితే', 'ఎందుకంటే']

# Remove stopwords from text
text = "నేను ఈ రోజు చాలా సంతోషంగా ఉన్నాను కాబట్టి బయటకు వెళ్లాలనుకుంటున్నాను"
cleaned = rmtsw(text, script="telugu")
print(cleaned)  # రోజు సంతోషంగా బయటకు వెళ్లాలనుకుంటున్నాను

# Add custom stopwords
telugu_sw.add_stopwords(["రోజు"], script="telugu")

# Save to JSON
telugu_sw.save_to_json("custom_stopwords.json")
```

## Notes

- `tsw` is an alias for the `TeluguStopWords` class.
- `rmtsw` is an alias for the `remove_stopwords` function.
- Use `script="telugu"` for Telugu script or `script="english"` for transliterated stopwords.
- Stopwords are sorted to prioritize Telugu script characters for better usability.

## Project Structure

```
telugu-stopwords/
├── telugu_stopwords/
│   ├── __init__.py
│   ├── telugu_stopwords.py
├── tests/
│   ├── test_telugu_stopwords.py
├── LICENSE
├── README.md
├── pyproject.toml
```

## Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/PavanYellathakota/telugu-stopwords.git
   cd telugu-stopwords
   ```

2. Update `pyproject.toml`:

   - Ensure `project.authors` has valid names and email addresses (e.g., `name = "Pavan Yellathakota", email = "pavanyellathakota@gmail.com"`).

3. Install dependencies:

   ```bash
   pip install pytest
   pip install -e .
   ```

4. Run tests:

   ```bash
   pytest tests/
   ```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make changes and commit (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please include tests for new features and follow the code of conduct.

## Testing

Run tests using pytest from the project root:

```bash
pytest tests/
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or suggestions, open an issue or contact:

- Pavan Yellathakota: pavanyellathakota@gmail.com
- Prudhvi Yellathakota: prudhviyellathakota@gmail.com