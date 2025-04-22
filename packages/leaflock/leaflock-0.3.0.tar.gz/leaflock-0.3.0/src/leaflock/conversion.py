import uuid

from .pydantic_models import Activity as PydanticActivity
from .pydantic_models import Textbook as PydanticTextbook
from .pydantic_models import Topic as PydanticTopic
from .sqlalchemy_tables import Activity as SQLActivity
from .sqlalchemy_tables import Textbook as SQLTextbook
from .sqlalchemy_tables import Topic as SQLTopic


def sqla_to_pydantic(sqla_textbook: SQLTextbook) -> PydanticTextbook:
    return PydanticTextbook(
        guid=sqla_textbook.guid,
        title=sqla_textbook.title,
        prompt=sqla_textbook.prompt,
        authors=sqla_textbook.authors,
        reviewers=sqla_textbook.reviewers,
        status=sqla_textbook.status,
        edition=sqla_textbook.edition,
        schema_version=sqla_textbook.schema_version,
        attributes=sqla_textbook.attributes,
        activities=[
            PydanticActivity(
                guid=activity.guid,
                name=activity.name,
                description=activity.description,
                prompt=activity.prompt,
                topics=set([topic.guid for topic in activity.topics]),
                sources=activity.sources,
                authors=activity.authors,
                license=activity.license,
            )
            for activity in sqla_textbook.activities
        ],
        topics=[PydanticTopic.model_validate(topic) for topic in sqla_textbook.topics],
    )


def pydantic_to_sqla(pydantic_textbook: PydanticTextbook) -> SQLTextbook:
    topics: list[SQLTopic] = list()
    for pydantic_topic in pydantic_textbook.topics:
        sql_topic = SQLTopic(
            name=pydantic_topic.name,
            outcomes=pydantic_topic.outcomes,
            summary=pydantic_topic.summary,
            sources=pydantic_topic.sources,
            authors=pydantic_topic.authors,
            license=pydantic_topic.license,
        )
        sql_topic.guid = pydantic_topic.guid
        topics.append(sql_topic)

    topics_by_guid: dict[uuid.UUID, SQLTopic] = {topic.guid: topic for topic in topics}

    activities: list[SQLActivity] = list()
    for pydantic_activity in pydantic_textbook.activities:
        sql_activity = SQLActivity(
            name=pydantic_activity.name,
            description=pydantic_activity.description,
            prompt=pydantic_activity.prompt,
            sources=pydantic_activity.sources,
            authors=pydantic_activity.authors,
            license=pydantic_activity.license,
        )

        for guid in pydantic_activity.topics:
            topic = topics_by_guid.get(guid)
            if topic is None:
                raise ValueError(f"No SQLTopic with guid: {guid}")
            sql_activity.topics.add(topic)

        sql_activity.guid = pydantic_activity.guid
        activities.append(sql_activity)

    return SQLTextbook(
        title=pydantic_textbook.title,
        prompt=pydantic_textbook.prompt,
        authors=pydantic_textbook.authors,
        reviewers=pydantic_textbook.reviewers,
        status=pydantic_textbook.status,
        edition=pydantic_textbook.edition,
        schema_version=pydantic_textbook.schema_version,
        attributes=pydantic_textbook.attributes,
        activities=activities,
        topics=topics,
    )
