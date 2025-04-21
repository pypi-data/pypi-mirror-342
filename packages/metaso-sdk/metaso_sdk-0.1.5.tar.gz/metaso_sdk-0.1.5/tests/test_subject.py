from streamable import Stream

from metaso_sdk.model import Query, Topic
from metaso_sdk.search import search
from metaso_sdk.subject import create_topic, delete_file, delete_topic, update_progress, upload_directory

from . import FIXTURES_DIR


def test_subject():
    topic = create_topic(Topic(name="functional programing"))
    files = upload_directory(topic, FIXTURES_DIR)

    assert sorted(file.fileName for file in files) == ["eurosys16-final29.pdf", "functions.pdf", "phd-thesis.pdf"]

    while True:
        if (
            Stream(files)
            .filter(lambda f: f.progress < 100)
            .throttle(per_second=1)
            .foreach(update_progress)
            .observe("progress update")
            .catch(finally_raise=True)
            .count()
            == 0
        ):
            break

    query = Query(question="functional")
    assert query.question in search(query, topic=topic)["text"]

    Stream(files).foreach(delete_file)()
    delete_topic(topic)
