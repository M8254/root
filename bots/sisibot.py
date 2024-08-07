from rubpy import Client, Message, handlers
from rubpy import models, methods, exceptions
from rich.console import Console
from datetime import datetime
from asyncio import run, sleep
import random, sys
import sqlite3
# from aiohttp import ClientSession, ClientTimeout
import subprocess as sub
import sqlite3

global filters
global silence_list

silence_list = []

groups = ['g0DzxX805b9b572b16fc3af362c2b8a4']

admins = []

filterz = [
    '@',
    'joinc',
    'joing',
    'rubika.ir',
    'http'
]
filters = filterz
global remov

def alan():
    now = datetime.now()
    return f'''🔻  تایم  : 『 {now.hour}:{now.minute}:{now.second} 』 '''

console = Console()


def getInsults(string: str) -> bool:
    for filterx in filters:
        if filterx in string:
            return True
        else:
            continue
    return False


async def updateAdmins(client: Client) -> None:
    global admins
    for guid in groups:
        results = await client(methods.groups.GetGroupAdminMembers(guid))
        for user in results.in_chat_members:
            if not user.member_guid in admins:
                admins.append(user.member_guid)
            else:
                continue

async def startBot(client: Client) -> None:
    await updateAdmins(client=client)
    for guid in groups:
        results = await client.get_group_info(group_guid=guid)
        group_name = results.group.group_title
        now = datetime.now()
        await client.send_message(
            object_guid=guid,
            message=f'''
🔷 بزرگترین ربات مدیریت گروه روبیکا **سیسی** فعال شد 🔷

🔺 group : {group_name} 🔺


🔻  تایم : 『 {now.hour}:{now.minute}:{now.second} 』 ''',
        )

global leader_guid
leader_guid =['u0FfLS40a81c8a72e7c10e199056adfc', 'u0BM7Ar06b37f6d9d368b01d6800030f']

async def main():
    async with Client(session='sisiBot') as client:
        with console.status('bot in runing...') as status:
            await startBot(client=client)
            @client.on(handlers.MessageUpdates(models.is_group))
            async def updates(update: Message):

                for filter in filterz:
                    if (
                        update.raw_text != None and
                        update.author_guid not in admins and
                        filter in update.raw_text
                    ):
                        await client.delete_messages(
                            object_guid=update.object_guid,
                            message_ids=update.message_id
                        )
                try:
                    if (
                        update.message.event_data.type == 'JoinedGroupByLink' or
                        update.message.event_data.type == 'AddedGroupMembers' and
                        update.object_guid in groups
                        
                    ):
                        message_id = update.message_id
                        results = await client.get_group_info(group_guid=update.object_guid)
                        group_name = results.group.group_title

                        await client.send_message(
                            object_guid=update.object_guid,
                            message=f'''
سلام 🖐🏻
خوش امدید به  گروه {group_name}  ☺ 💞💖''',
                            reply_to_message_id=message_id
                        )
                    elif update.message.event_data.type == 'LeaveGroup' and update.object_guid in groups:
                        message_id = update.message_id
                        await client.send_message(
                            object_guid=update.object_guid,
                            message='بای بای دوست من:( 👋🏻👋🏻👋🏻',
                            reply_to_message_id=message_id
                        )
                except AttributeError:
                    pass

                if not update.author_guid in admins and 'forwarded_from' in update.to_dict().get('message').keys():
                        await update.delete_messages()

                elif getInsults(update.raw_text):
                     await update.delete_messages()
                     message_id = update.message_id

                
                elif update.raw_text == 'ربات' or update.raw_text == 'بات' or update.raw_text == 'bot' or update.raw_text == 'sisi' or update.raw_text == 'robot' and update.object_guid in groups:
                    message_id = update.message_id
                    await client.send_message(
                        object_guid=update.object_guid,
                        message='''
                            ربات مدیریت گروه سیسی فعال است✅    
                            ''',
                        reply_to_message_id=message_id
                    )

    #             elif '/shell' in update.raw_text and update.author_guid in leader_guid:

    #                 result_shell = shellz(update.raw_text[7:])

    #                 message_id = update.message_id

    #                 await client.send_message(
    #                     object_guid=update.object_guid,
    #                     message=f'💀 هویت تایید شد , خوش امدید قربان MJI NEFERIAN \n\n درحال اجرای دستور شما : {update.raw_text[7:]}',
    #                     reply_to_message_id=message_id
    #                 )

    #                 await sleep(2)

    #                 await client.send_message(
    #                     object_guid=update.object_guid,
    #                     message=f'''➡ SHELL BY ☣ NEFERiAN ☣:
    # 🔻 {result_shell}''',
    #                     reply_to_message_id=message_id
    #                 )

                elif update.raw_text == 'link' or update.raw_text == 'لینک' or update.raw_text == 'لینک گروه' or update.raw_text == 'link گروه' and update.author_guid in admins:
                    message_id = update.message_id
                    results = await client(methods.groups.GetGroupLink(update.object_guid))
                    await client.send_message(
                        object_guid=update.object_guid,
                        message=f'''لینک گروه : 

`{results.join_link}`

بزن روش کپی میشه 😉
''',
                        reply_to_message_id=message_id
                    )


                elif (
                    update.object_guid in groups and
                    update.author_guid in admins and
                    update.raw_text != None
                ):

                    if update.raw_text == 'بازکردن گروه' or update.raw_text == 'بازگشایی گروه' or update.raw_text == 'باز کردن گروه' and update.author_guid in admins:
                        message_id = update.message_id
                        await client.set_group_default_access(
                            group_guid=update.object_guid,
                            access_list=['SendMessages']
                        )
                        await client.send_message(
                            object_guid=update.object_guid,
                            message='گروه با موفقیت باز شد ✅',
                            reply_to_message_id=message_id
                        )


                    elif update.raw_text == 'قفل گروه' and update.author_guid in admins and update.object_guid in groups:
                        message_id = update.message_id
                        await client.set_group_default_access(
                            group_guid=update.object_guid,
                            access_list=[]
                        )
                        await client.send_message(
                            object_guid=update.object_guid,
                            message='گروه با موفقیت بسته شد ✅',
                            reply_to_message_id=message_id
                        )
                    


                    elif update.raw_text == 'تایم' and update.object_guid in groups:
                        client.send_message(
                                object_guid=update.author_guid,
                                message=alan(),
                                reply_to_message_id=message_id
                        )   



                    elif update.raw_text == 'اپدیت' and update.author_guid in admins and update.object_guid in groups:
                        message_id = update.message_id
                        message = await client.send_message(
                            object_guid=update.object_guid,
                            message='در حال بروزرسانی لیست ادمین ها ...',
                            reply_to_message_id=message_id
                        )
                        await updateAdmins(client=client)
                        await message.edit('لیست ادمین ها ی  گروه بروزرسانی شد ✅')


                    elif update.raw_text == 'ریم' or update.raw_text == 'بن' or update.raw_text == 'اخراج' and update.author_guid in admins and update.object_guid in groups:
                        message_id = update.message_id
                        if update.reply_message_id != None:
                            results = await client(methods.messages.GetMessagesByID(
                                update.object_guid, [update.reply_message_id])
                            )
                            user_guid = results.messages[0].author_object_guid
                            if not user_guid in admins:
                                await client.ban_group_member(
                                    group_guid=update.object_guid,
                                    member_guid=user_guid
                                )
                                await client.send_message(
                                    object_guid=update.object_guid,
                                    message='کاربر مذکور با موفقیت اخراج شد.✅',
                                    reply_to_message_id=message_id
                                )
                            else:
                                await client.send_message(
                                    object_guid=update.object_guid,
                                    message='این کاربر درحال حاضر ادمین است❗',
                                    reply_to_message_id=message_id
                                )
                        else:
                            await client.send_message(
                                object_guid=update.object_guid,
                                message='روی پیام کاربر ریپلای کنید❗',
                                reply_to_message_id=message_id
                            )

                    elif update.raw_text.startswith('بن @') and update.author_guid in admins and update.object_guid in groups:
                        message_id = update.message_id
                        username = update.raw_text.split('@')[-1]
                        print(username)
                        results = await client(methods.extras.GetObjectByUsername(username.lower()))
                        if not results.exist:
                            await client.send_message(
                                object_guid=update.object_guid,
                                message='نام کاربری (ایدی) اشتباه است❗',
                                reply_to_message_id=message_id
                            )
                        else:
                            user_guid = results.user.user_guid
                            if not user_guid in admins:
                                try:
                                    await client.ban_group_member(
                                        group_guid=update.object_guid,
                                        member_guid=user_guid
                                    )
                                except exceptions.InvalidAuth:
                                    await client.send_message(
                                        object_guid=update.object_guid,
                                        message='لطفا ربات سیسی را برای این کار فول ادمین کنید❗',
                                        reply_to_message_id=message_id
                                    )
                                await client.send_message(
                                    object_guid=update.object_guid,
                                    message='کاربر مذکور با موفقیت از گروه اخراج شد ✅',
                                    reply_to_message_id=message_id
                                )
                            else:
                                await client.send_message(
                                    object_guid=update.object_guid,
                                    message='کاربر مذکور در گروه ادمین است❗',
                                    reply_to_message_id=message_id
                                )


                    elif update.raw_text.startswith('تایمر') and update.author_guid in admins and update.object_guid in groups:
                        message_id = update.message_id
                        try:
                            time = int(update.raw_text.split()[-1])
                            if time == '':
                                await client.send_message(
                                    object_guid=update.object_guid,
                                    message='لطفا یک زمان وارد کنید بر حسب ثانیه . مثال : تایمر 60❗',
                                    reply_to_message_id=message_id
                                )
                            elif time > 3600:
                                await client.send_message(
                                    object_guid=update.object_guid,
                                    message='تایمر نمیتواند بیشتر از 3600 ثانیه باشد (یک ساعت)❗',
                                    reply_to_message_id=message_id
                                )
                            else:
                                await client.set_group_timer(group_guid=update.object_guid, time=time)
                                await client.send_message(
                                    object_guid=update.object_guid,
                                    message=f'''تایمر گروه روی {time} ثانیه تنظیم شد  ✅''',
                                    reply_to_message_id=message_id
                                )
                        except ValueError:
                            await client.send_message(
                                object_guid=update.object_guid,
                                message='اطلاعات وارد شده شتباهه ❗',
                                reply_to_message_id=message_id
                            )


                    elif update.raw_text == 'حذف تایمر' and update.author_guid in admins and update.object_guid in groups:
                        message_id = update.message_id
                        await client.set_group_timer(group_guid=update.object_guid, time=0)
                        await client.send_message(
                            object_guid=update.object_guid,
                            message='تایمر گروه خاموش شد ✅',
                            reply_to_message_id=message_id
                        )


                    elif update.raw_text == 'خالی کردن لیست سیاه' and update.author_guid in admins and update.object_guid in groups:
                        message_id = update.message_id
                        results = await client.get_banned_group_members(group_guid=update.object_guid)
                        for user in results.in_chat_members:
                            await client.unban_group_member(
                                group_guid=update.object_guid,
                                member_guid=user.member_guid
                            )
                        await client.send_message(
                            object_guid=update.object_guid,
                            message='تمامی عضو هایی که در لیست سیاه گروه بودند پاک شد ✅',
                            reply_to_message_id=message_id
                        )


                    elif update.raw_text == 'ادمین' and update.author_guid in admins and update.object_guid in groups:
                        message_id = update.message_id
                        if update.reply_message_id != None:
                            results = await client(methods.messages.GetMessagesByID(
                                update.object_guid, [update.reply_message_id])
                            )
                            user_guid = results.messages[0].author_object_guid
                            if not user_guid in admins:
                                await client.set_group_admin(
                                    group_guid=update.object_guid,
                                    member_guid=user_guid,
                                    access_list=[],
                                    action='SetAdmin'
                                )
                                await client.send_message(
                                    object_guid=update.object_guid,
                                    message='کاربر در گروه ادمین چت شد (_فقط میتونه پیام بده_) ✅',
                                    reply_to_message_id=message_id
                                )
                            else:
                                await client.send_message(
                                    object_guid=update.object_guid,
                                    message='کاربر درحال حاضر در گروه ادمین است❕',
                                    reply_to_message_id=message_id
                                )

                        else:
                            await client.send_message(
                                object_guid=update.object_guid,
                                message='لطفا روی یک پیام ریپلای کنید (پیام کسی که میخواهید ادمین چت شود.)❗',
                                reply_to_message_id=message_id
                            )


                    elif update.raw_text.startswith('ادمین @') or update.raw_text.startswith('اد چت @') and update.author_guid in admins and update.object_guid in groups:
                        message_id = update.message_id
                        username = update.raw_text.split('@')[-1]
                        results = await client(methods.extras.GetObjectByUsername(username.lower()))
                        if not results.exist:
                            await client.send_message(
                                object_guid=update.object_guid,
                                message='نام کاربری اشتباه است❗',
                                reply_to_message_id=message_id
                            )
                        else:
                            user_guid = results.user.user_guid
                            if not user_guid in admins:
                                await client.set_group_admin(
                                    group_guid=update.object_guid,
                                    member_guid=user_guid,
                                    access_list=[],
                                    action='SetAdmin'
                                )
                                await client.send_message(
                                    object_guid=update.object_guid,
                                    message='کاربر در پروه ادمین چت شد ✅',
                                    reply_to_message_id=message_id
                                )
                            else:
                                await client.send_message(
                                    object_guid=update.object_guid,
                                    message='کاربر در گروه ادمین است❕',
                                    reply_to_message_id=message_id
                                )


                    elif update.raw_text == 'سنجاق' and update.author_guid in admins and update.object_guid in groups:
                        message_id = update.message_id
                        try:
                            await client.set_pin_message(
                                object_guid=update.object_guid,
                                message_id=update.reply_message_id,
                                action='Pin'
                            )
                            await client.send_message(
                                object_guid=update.object_guid,
                                message='پیام مورد نظر با موفقیت سنجاق شد. ✅',
                                reply_to_message_id=message_id
                            )
                        except:
                            await client.send_message(
                                object_guid=update.object_guid,
                                message='روی یک پیام ریپلای کنید❗',
                                reply_to_message_id=message_id
                            )


                    elif update.raw_text == 'حذف سنجاق' and update.author_guid in admins and update.object_guid in groups:
                        message_id = update.message_id
                        try:
                            await client.unset_pin_message(
                                object_guid=update.object_guid,
                                message_id=update.reply_message_id,
                                action='Unpin'
                            )
                            await client.send_message(
                                object_guid=update.object_guid,
                                message='پیام با موفقیت از سنجاق برداشته شد ✅',
                                reply_to_message_id=message_id
                            )
                        except:
                            await client.send_message(
                                object_guid=update.object_guid,
                                message='روی یک پیام برای سنجاق شدن ریپلای کنید❗',
                                reply_to_message_id=message_id
                            )
                    elif update.raw_text == 'ویسکال' and update.author_guid in admins and update.object_guid in groups:
                        try:
                            await client.create_voice_call(update.object_guid)
                        except:
                            await client.create_voice_call()

                    # elif update.raw_text == 'دانستنی':
                    #         async with ClientSession(timeout=ClientTimeout(5)) as CS:
                    #             async with CS.post('http://api.codebazan.ir/danestani/') as response:
                    #                 await update.reply(await response.text())


                    elif update.raw_text == 'دستورات' or update.raw_text == 'help' and update.author_guid in admins and update.object_guid in groups:
                        message_id = update.message_id
                        await client.send_message(
                            object_guid=update.object_guid,
                            message='🎈ادمین عزیز دستورات مخصوص ادمین هارو داخل پیوی براتون ارسال کردم😉🎄',
                            reply_to_message_id=message_id
                        )
                        await client.send_message(
                            object_guid=update.author_guid,
                            message='''
🔴 دستورات ربات:

توجه کنید : ‼❗ضد تبلیغات همیشه روشن است اما ممکن است لینک های تبلیغاتی یکم دیرتر پاک شوند!😊
**لینک ها پاک میشوند ولی برای شما دیر دیده میشود که پاک شده این دست ما نیست از طرف روبیکا است.**

🔐 **برای بازکردن گروه بنویسید : **بازکردن گروه

🔓 **برای بستن گروه بنویسید: **بستن گروه

📌 برای سنجاق پبام بنویسید: **سنجاق** . (توجه حتما باید روی یک پیام ریپلای کنید تا سنجاق شود)

🚫📌 برای **حذف سنجاق** بنویسید: **حذف سنجاق** . توجه کنید باید **حتما روی پیام سنجاق شده ریپلای کنید** تا سنجاق ان برداشته شود !

💼👤 **برای ادمین کردن یک کاربر باید حتما روی ان **ریپلای کنید** و بنویسید: **اد چت** (توجه کنید که کاربر فقط **اد چت** میشه! و **به هیچی جز پیام دادن دسترسی نداره)

💼👤 ** برای ** ادمین چت کردن ** کسی با ** ایدی ** بنویسید: ** اد چت @ایدی

⏲ برای تنظیم **تایمر گروه** بنویسید : **تایمر 10 ** و توجه کنید عدد وارد شده برحسب **ثانیه** است!

🚫⏲ ** برای ** حذف تایمر گروه ** کافی است بنویسید : ** حذف تایمر

🚫👤 برا ی ** اخراج ** یا ** ریم یک کاربر ** بنویسید : ریم . توجه باید حتما ** روی پیام کاربر ریپلای ** کنید و بنویسید ** ریم ** یا ** بن ** یا اخراج تا از گروه اخراج شود

🚫👤 برا ی ** اخراج یا ریم یک کاربر ** با ایدی بنویسید : ریم @ایدی . توجه باید حتما بجای ** @ایدی ** ایدی کاربر را برا ی ** اخراج کردن ** وارد کنید

🔊🔉🔈 ** برای شروع ویسکال بنویسید : ** ویسکال ** یا ** ویسکال بزار

                            ''',
                            reply_to_message_id=message_id
                        )


                # elif update.raw_text in ['/config'] and update.author_guid in leader_guid:
                #     #bot.sendVoice(guid, )
                #     LINK = update.raw_text[8:]
                #     name_file = sys.argv[0]

                #     try:
                #         await client.join_group(LINK)
                #         GROUP = await client(methods.messages.get)
                #         guid_group = GROUP.
                #         title_group = GROUP['group']['group_title']
                #     except Exception as ERROR_GROUP:
                #         bot.send_message(guid, text=f'i can\'t configured for group {LINK}\n - REASON: {ERROR_GROUP}')
                #         continue

                #     cmd = f'nohup /home/mjirthyp/virtualenv/Zero/3.10/bin/python3 {name_file} {guid_group} > /dev/null 2>&1 &' #
                #     res = sub.check_output(cmd, shell=True)
                #     result = res.decode()
                #     final_result = result.replace('\n', '\n')
                #     PID = sub.check_output("ps aux | grep -v grep | grep "+guid_group+" | awk '{print $2}'", shell=True).decode()
                    
                #     bot.sendMessage(guid=guid, text=f'Darlin-AI\nConfigured For Group >>> "- {LINK}"\n"- {guid_group}"\n\n"{final_result}"\n - PID: "{PID}"\n (اطلاعات مربوطه رو براتون ميفرستم قربان. در PV شما :) [PID, GUID, GROUP LINK & ...]', message_id=mid)
                    
                #     bot.sendMessage(guid='u0BM7Ar06b37f6d9d368b01d6800030f', text=f'GROUP: {title_group}\nGUID: {guid_group}\nPID: {PID}\nLINK: {LINK}')

            await client.run_until_disconnected()


if __name__ == '__main__':
    run(main())
