from model import Triples_extract
from language_detecter import detect_language

relations = "has_advantage_in;has_problem_in;is_methods_of"

subject_type = "device;advantages;issue;methods"

object_type = "device;advantages;issue;methods"

corpus_path = "corpus.txt"
extracted_triples_path = "extracted_triples.txt"




if detect_language(corpus_path) == 0:
    l = "Chinese"
else:
    l = "English"

with open(corpus_path,"rb") as f:
    s = f.read()


if __name__ == "__main__":

    input_data={

        "sentence":s,
        "language":l,
        "relations":relations,
        "object_type":object_type,
        "subject_type":subject_type         
    }

    result = Triples_extract(input_data,extracted_triples_path)
    print(result)
