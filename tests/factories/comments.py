import factory

from app.schemas.comments import CreateCommentSchema


class CommentFactory(factory.Factory):
    content = factory.Faker("sentence", nb_words=10)

    class Meta:
        model = CreateCommentSchema
