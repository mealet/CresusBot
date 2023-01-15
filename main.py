import disnake
from disnake.ext import commands
from disnake.ui import Button
from disnake import ButtonStyle
from disnake import TextInputStyle
import datetime
import os

intents = disnake.Intents.all()
command_sync_flags = commands.CommandSyncFlags.none()
command_sync_flags.sync_commands = True
bot = commands.Bot(command_prefix="!",
                   intents=intents,
                   test_guilds=[974385691272302592],
                   command_sync_flags=command_sync_flags)
global start_time
start_time = datetime.datetime.now()


@bot.event
async def on_ready():
  print("[SYSTEM][ON_READY]: Бот запущен")


@bot.event
async def on_message(message):
  print(
    f"[DISCORD][MESSAGE][{message.channel.name}] {message.author.name}: {message.content}"
  )


@bot.slash_command(name="ping",
                   description="Проверка на стабильную работу бота")
@commands.has_permissions(administrator=True)
async def ping(inter):
  try:
    ping_embed = disnake.Embed(title="Информация о работе бота",
                               description="Cresus Bot",
                               color=disnake.Colour.green(),
                               timestamp=datetime.datetime.now())
    ping_embed.add_field(
      name="Время работы",
      value=
      f"Начало работы бота: {start_time}\nВремя работы: {datetime.datetime.now() - start_time}"
    )
    ping_embed.add_field(name="Текущий сервер",
                         value=f"Название: {bot.guilds[0]}")
    ping_embed.add_field(name="Пинг WebSocket-а", value=f"Пинг: {bot.latency}")
    await inter.response.send_message(
      "Информация и панель управления отправлена в личные сообщения")
    if inter.author.id == 526367373473742858:
      await inter.author.send(embed=ping_embed,
                              components=[
                                disnake.ui.Button(
                                  style=disnake.ButtonStyle.red,
                                  label="Остановить бота",
                                  disabled=False,
                                  custom_id='stop_bot_btn')
                              ])

      response = await bot.wait_for("button_click")
      if response.component.custom_id == "stop_bot_btn":
        await inter.author.send("Бот успешно остановлен!")
        quit()
    else:
      await inter.author.send(embed=ping_embed)

  except PermissionError:
    await inter.response.send_message(
      "Недостаточно прав\nОбязательные права для выполнения данной команды: Administrator"
    )


#modal windows


class KitModal(disnake.ui.Modal):

  def __init__(self):
    components = [
      disnake.ui.TextInput(label="Ваше Имя",
                           custom_id="kit_project_name",
                           style=TextInputStyle.short,
                           max_length=50),
      disnake.ui.TextInput(label="Ваш возраст",
                           custom_id="kit_project_old",
                           style=TextInputStyle.short,
                           max_length=5),
      disnake.ui.TextInput(label="Наличие микрофона",
                           custom_id="kit_project_micro",
                           style=TextInputStyle.short,
                           max_length=4),
      disnake.ui.TextInput(label="Ник в Minecraft",
                           custom_id="kit_project_nick",
                           style=TextInputStyle.short,
                           max_length=50)
    ]
    super().__init__(title="Заявка на проект CresusCraft",
                     components=components,
                     custom_id="kit_project_registration",
                     timeout=600)

  async def callback(self, inter: disnake.ModalInteraction):
    channel = bot.get_channel(1063753297665736735)
    emb = disnake.Embed(title="Заявка на проект CresusCraft",
                        color=disnake.Colour.green(),
                        description=f"Заявку отправил: {inter.author.mention}")

    print(f"[CALLBACK][KIT_PROJECT] Полученые данные: {inter.text_values}")
    emb.add_field(name="Имя",
                  value=inter.text_values["kit_project_name"],
                  inline=False)
    emb.add_field(name="Возраст",
                  value=inter.text_values["kit_project_old"],
                  inline=False)
    emb.add_field(name="Наличие микрофона",
                  value=inter.text_values["kit_project_micro"],
                  inline=False)
    emb.add_field(name="Никнейм в Minecraft",
                  value=inter.text_values["kit_project_nick"],
                  inline=False)

    await inter.response.send_message(
      f"{inter.author.mention} | Заявка отправлена. Ожидайте првоерки, вам напишут в личные сообщения.\n`Комманда регистрации /reg`"
    )
    await channel.send(embed=emb)


class LogModal(disnake.ui.Modal):

  def __init__(self):
    components = [
      disnake.ui.TextInput(label="Сфера действий",
                           custom_id="a_sphere",
                           style=TextInputStyle.short,
                           max_length=50,
                           placeholder="Discord/Server/Design"),
      disnake.ui.TextInput(label="Лог действий",
                           custom_id="a_log",
                           style=TextInputStyle.paragraph)
    ]
    super().__init__(title="Запись в архив",
                     components=components,
                     custom_id="archive")

  async def callback(self, inter: disnake.ModalInteraction):
    emb = disnake.Embed(title="Запись в архив",
                        description=f"Автор: {inter.author.mention}",
                        timestamp=datetime.datetime.now(),
                        color=disnake.Colour.green())

    emb.add_field(name="Сфера действий", value=inter.text_values["a_log"])

    await inter.response.send_message(embed=emb)
    await inter.response.send_message("Запись успешно создана", ephemeral=True)


@bot.slash_command(name="archive", description="Запись лог действий в архив")
@commands.has_permissions(administrator=True)
async def archive(inter):
  if inter.channel.id == 974402891701973032:
    await inter.response.send_modal(modal=LogModal())
  else:
    await inter.response.send_message(
      "Данная комманда предназначена для канала <#974402891701973032>",
      ephemeral=True)


@bot.slash_command(name="reg", description="Регистрация на проект")
async def reg(inter):
  if inter.channel.id == 1059752620127965285:
    try:
      await inter.response.send_modal(modal=KitModal())
    except:
      await inter.response.send_message("Произошла ошибка!", ephemeral=True)

  else:
    await inter.response.send_message(
      "Комманда создана для канала <#1059752620127965285>", ephemeral=True)


bot.run("MTA2MTY3MzQ1NjY5OTE4MzIyNw.G43uc2.-V2tlAhBhvaLcW_4C1YmGbb2IHDnbRG1nH167A")
