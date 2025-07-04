import logging
import os
from typing import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from aiogram import Dispatcher, Bot
from aiogram.types import Update
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from handlers import setup_routers
from config_reader import config


os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(funcName)s) %(message)s",
    handlers=[
        logging.FileHandler("logs/logs.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    webhook_url = f"{config.WEBHOOK_URL.get_secret_value()}/webhook"
    
    await bot.set_webhook(
        url=f"{webhook_url}",
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )
    
    yield
    
    
bot = Bot(
        token=config.BOT_TOKEN.get_secret_value(), 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )


dp = Dispatcher(storage=MemoryStorage())

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

dp.include_router(setup_routers())
    

@app.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(config.WEBHOOK_PORT.get_secret_value()))
