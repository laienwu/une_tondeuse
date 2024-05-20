Assuming `poetry` is installed

Go to `ps_mower` folder

The expected outcome regarding the instructions is run through the `test_instruction` test located in `test/test_mow.py`

```bash
poetry install
pytest -rP --cov-report html  --cov=tondeuse tests/

