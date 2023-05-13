@ECHO ON
call git pull
call conda activate ./env
call python -m uvicorn main:app --port 22702
@cmd /k