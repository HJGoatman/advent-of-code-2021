FROM python
WORKDIR /aoc-2021
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "18.py", "test.txt"]