from aiomodels.contents.image_content import ImageContent
from aiomodels.contents.text_content import TextContent
from aiomodels.sources.base64_source import Base64Source


def test_text_content_creation():
    content = TextContent(text="Hello!")
    assert content.text == "Hello!"
    assert content.type == "text"


def test_image_content_creation():
    content = ImageContent(source=Base64Source(data="abc", media_type="image/png"), detail="low")
    assert content.source.url == "data:image/png;base64,abc"
    assert content.detail == "low"
    assert content.type == "image"
