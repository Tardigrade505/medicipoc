MKDIR endpoints-python
CD endpoints-python
pip install --target ./package pymysql
CD package
7z a ../../endpoints-python.zip .
cd ../..
7z u endpoints-python.zip *.py
RMDIR /S/Q endpoints-python