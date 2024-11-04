import factory

from app.schemas.posts import CreatePostSchema


class PostFactory(factory.Factory):
    title = factory.Faker("sentence", nb_words=6)
    content = factory.Faker("paragraph", nb_sentences=5)

    class Meta:
        model = CreatePostSchema
