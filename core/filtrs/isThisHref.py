
from aiogram.types import Message
from aiogram.enums.message_entity_type import MessageEntityType
from aiogram.filters import BaseFilter

class FilterLinks(BaseFilter):
    async def __call__(self, message: Message):
        if msg_entities := (message.entities or message.caption_entities):
            entities = []
            for entitie in msg_entities:
                if entitie.type in [MessageEntityType.URL, MessageEntityType.TEXT_LINK]:
                    print(str(entitie))
                    entities.append(entitie)
            # этот словарь идет в хендлер ниже
            return {"entities": entities} if entities else False
        else:
            await message.answer('о пезда')


class IsThisHref(BaseFilter):
    async def __call__(self, message:Message):
        pass
