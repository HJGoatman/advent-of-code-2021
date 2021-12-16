FROM python
WORKDIR /aoc-2021
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "16.py", "input.txt"]