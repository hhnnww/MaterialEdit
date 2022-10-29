@ECHO ON
call conda activate FTDesign
call python -m uvicorn main:app --port 22702
@cmd /k