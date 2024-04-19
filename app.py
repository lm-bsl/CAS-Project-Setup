import os
from flask import Flask, jsonify, render_template, request, send_file

from chatbot.chatbot import Chatbot


PYTHONANYWHERE_USERNAME = "carvice"
PYTHONANYWHERE_WEBAPPNAME = "mysite"

app = Flask(__name__)
app.debug = os.getenv('FLASK_DEBUG') == '1'

my_type_role = """
   Develop an adaptive dialogue system: Design the system to respond to user replies by generating more precise follow-up questions. 
   Utilize a large language model (LLM) to analyze the context and meaning of user responses. 
   Employ this technology to create intelligent questioning strategies that assist users in recalling elusive memories.
"""

my_instance_context = """
 
"""
variantA = """
 Additionally, ensure that the system generates open-ended questions to guide the user in exploring their memories.
 This approach will encourage more detailed responses and facilitate deeper reflection.
Adding this extension will help the chatbot facilitate a deeper and more reflective conversation, ideally leading to a richer recollection of memories by the user.

"""

variantB = """
   When interacting with the user, always ask questions that can be answered with a simple yes or no to streamline communication and maintain clarity.
"""

my_instance_starter = """
Great the user in a welcoming and engaging and help him remember!
"""

bot = Chatbot(
    database_file="database/chatbot.db",
    type_id="base",
    user_id="user1",
    type_name="Base Assistant",
    type_role=my_type_role,
    instance_context=my_instance_context,
    instance_starter=my_instance_starter
)

bot.start()
bot.reset()



bot = Chatbot(
    database_file="database/chatbot.db",
    type_id="varianta",
    user_id="user2",
    type_name="Assistant Variant A",
    type_role=my_type_role,
    instance_context=variantA,
    instance_starter=my_instance_starter
)
bot.start()
bot.reset()

bot = Chatbot(
    database_file="database/chatbot.db",
    type_id="variantb",
    user_id="user3",
    type_name="Assistant Variant B",
    type_role=my_type_role,
    instance_context=variantB,
    instance_starter=my_instance_starter
)

bot.start()

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/mockups.pdf', methods=['GET'])
def get_first_pdf():
    script_directory = os.path.dirname(os.path.realpath(__file__))
    files = [f for f in os.listdir(script_directory) if os.path.isfile(os.path.join(script_directory, f))]
    pdf_files = [f for f in files if f.lower().endswith('.pdf')]
    if pdf_files:
        # Get the path to the first PDF file
        pdf_path = os.path.join(script_directory, pdf_files[0])

        # Send the PDF file as a response
        return send_file(pdf_path, as_attachment=True)

    return "No PDF file found in the root folder."


@app.route("/<type_id>/<user_id>/chat")
def chatbot(type_id: str, user_id: str):
    return render_template("chat.html")


@app.route("/<type_id>/<user_id>/comparison")
def chatbot_comp(type_id: str, user_id: str):
    return render_template("comparison.html")


@app.route("/bots")
def get_bots():
    bots = bot.get_all_bots()
    return jsonify(bots)


@app.route("/<type_id>/<user_id>/info")
def info_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: dict[str, str] = bot.info_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/conversation")
def conversation_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: list[dict[str, str]] = bot.conversation_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/response_for", methods=["POST"])
def response_for(type_id: str, user_id: str):
    user_says = None
    # content_type = request.headers.get('Content-Type')
    # if (content_type == 'application/json; charset=utf-8'):
    user_says = request.json
    # else:
    #    return jsonify('/response_for request must have content_type == application/json')

    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    assistant_says_list: list[str] = bot.respond(user_says)
    response: dict[str, str] = {
        "user_says": user_says,
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)


@app.route("/<type_id>/<user_id>/reset", methods=["DELETE"])
def reset(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    bot.reset()
    assistant_says_list: list[str] = bot.start()
    response: dict[str, str] = {
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)
