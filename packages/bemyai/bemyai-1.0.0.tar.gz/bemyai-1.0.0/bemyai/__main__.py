import sys
import argparse
import asyncio
import os
import os.path
from loguru import logger
from bemyai import BeMyAI  # type: ignore


async def _messages_receiver(p, bm, sid, chat_id):
    while True:
        async for bm_response in bm.receive_messages(sid):
            message = bm_response
            if message.user:
                continue
            print(message.data)
            break
        if p.ni:
            break
        print("Type    Q    and press enter for exit")
        text = input("Message:")
        if text.strip().lower() in ["q", "quit", "exit"]:
            break
        sid, chat_id, _message = await bm.send_text_message(chat_id, text)
        await asyncio.sleep(0.1)


async def a_main(args: list) -> None:
    parser = argparse.ArgumentParser(prog="bm")
    parser.add_argument(
        "--lang",
        "-l",
        dest="lang",
        default="en",
        metavar="en",
        help="Response language",
    )
    parser.add_argument(
        "--tokenfile",
        "-tf",
        dest="tokenfile",
        default=os.path.expanduser(os.path.join("~", "bm_token.txt")),
        metavar="bm_token.txt",
        help="the path to the file for storing the token from the account",
        type=argparse.FileType("a+b"),
    )
    parser.add_argument(
        "--sessionfile",
        "-sf",
        dest="sessionfile",
        default=os.path.expanduser(os.path.join("~", "bm_session.txt")),
        metavar="bm_session.txt",
        help="the path to the file for storing the session id",
        type=argparse.FileType("a+b"),
    )
    parser.add_argument(
        "--not-interactive",
        "-ni",
        dest="ni",
        action="store_true",
        help="Do not ask for user input",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Whether to enable logging?"
    )

    subparsers = parser.add_subparsers(dest="sub", help="Action")
    parser_login = subparsers.add_parser(
        "login", help="Log in to your account and get a token"
    )
    parser_login.add_argument("email", metavar="E-mail address")
    parser_login.add_argument("password", metavar="Password")

    parser_signup = subparsers.add_parser("signup", help="Create a new account")
    parser_signup.add_argument("first_name", metavar="First name")
    parser_signup.add_argument("last_name", metavar="Last name")

    parser_signup.add_argument("email", metavar="E-mail address")
    parser_signup.add_argument("password", metavar="Password")

    parser_reset_password = subparsers.add_parser(
        "reset-password",
        help="Forgot your password? Send a link to the password change form by email",
    )
    parser_reset_password.add_argument("email", metavar="E-mail address")

    subparsers.add_parser(
        "resend-verify-email", help="Send the confirmation email again"
    )

    parser_recognize = subparsers.add_parser(
        "recognize", help="Get a description for an image"
    )
    parser_recognize.add_argument("photo", type=argparse.FileType("rb"))

    parser_ask = subparsers.add_parser(
        "ask", help="Ask a question about recognized photo"
    )
    parser_ask.add_argument("text", help="message")

    p = parser.parse_args()
    if p.verbose:
        logger.remove()
        logger.add(sys.stderr, format="{time} {level} {message}", level="DEBUG")
    else:
        logger.remove()
    if p.sub == "login":
        bm = BeMyAI("", response_language=p.lang)
        result = await bm.login(email=p.email, password=p.password)
        p.tokenfile.seek(0)
        p.tokenfile.truncate()
        p.tokenfile.write(result.token.encode("UTF-8"))
        p.tokenfile.flush()

    if p.sub == "signup":
        bm = BeMyAI("", response_language=p.lang)
        result = await bm.signup(
            first_name=p.first_name,
            last_name=p.last_name,
            email=p.email,
            password=p.password,
        )
        p.tokenfile.seek(0)
        p.tokenfile.truncate()
        p.tokenfile.write(result.token.encode("UTF-8"))
        p.tokenfile.flush()

        sys.stderr.write("Don't forget to confirm your email address")

    if p.sub == "reset-password":
        bm = BeMyAI("", response_language=p.lang)
        await bm.send_reset_password(email=p.email)

    if p.sub == "resend-verify-email":
        p.tokenfile.seek(0)
        token = p.tokenfile.read().decode("UTF-8")
        bm = BeMyAI(token, response_language=p.lang)
        await bm.resend_verify_email()

    if p.sub == "recognize":
        p.tokenfile.seek(0)
        token = p.tokenfile.read().decode("UTF-8")
        bm = BeMyAI(token, response_language=p.lang)
        sid, chat_id = await bm.take_photo(p.photo)
        p.sessionfile.seek(0)
        p.sessionfile.truncate()
        p.sessionfile.write(str(chat_id).encode("UTF-8"))
        p.sessionfile.flush()
        await _messages_receiver(p, bm, sid, chat_id)
    if p.sub == "ask":
        p.sessionfile.seek(0)
        try:
            chat_id = int(p.sessionfile.read())
        except ValueError:
            sys.stderr.write("session id not found")
            sys.exit(2)
        p.tokenfile.seek(0)
        token = p.tokenfile.read().decode("UTF-8")
        bm = BeMyAI(token, response_language=p.lang)
        sid, chat_id, _message = await bm.send_text_message(chat_id, p.text)
        await _messages_receiver(p, bm, sid, chat_id)


def main(args: list = sys.argv) -> None:
    asyncio.run(a_main(args))


if __name__ == "__main__":
    main(sys.argv)
