from flask import Flask
from flask import render_template
import json
from flask import request,url_for
from pprint import pprint
from flask_weasyprint import HTML, render_pdf,CSS
from pyppeteer import launch
import asyncio
# import threading
# import multiprocessing
import subprocess
import concurrent.futures

app = Flask(__name__)

async def generate_pdf(html_content, pdf_path):
    browser = await launch()
    page = await browser.newPage()
    await page.setContent(html_content)
    await page.waitForSelector('body')
    await page.pdf({'path': pdf_path, 'format': 'letter'})
    await browser.close()

def generate_pdf_process(html_content, pdf_path):
    asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.get_event_loop().run_until_complete(generate_pdf(html_content, pdf_path))


def run_asyncio_loop(html_content, pdf_path):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(generate_pdf(html_content, pdf_path))
    loop.close()


@app.route("/", methods=["POST", "GET"])
def home_page():
	error = None
	if request.method == 'POST':
		print("-------------RECEIVED JSON INPUT---------")
		pprint(request.form)
		context = {}
		for key,value in request.form.items():
			k = key[-1]

			if context.get(k) is None:
				context[k] = {key[:-2] : value}
				work_desc = []
			else:
				if key[:-2] == "work_description":
					work_desc = value.split("\r\n")
					context[k].update({key[:-2] : work_desc})
				else:
					context[k].update({key[:-2] : value})
		list_c = list(context.values())
		# print("list c")
		# print(*list_c,sep="\n---\n")

		html_rendered = render_template("flask_template.html", work_experience = list_c)
		stylesheet = CSS(url_for('static', filename='weasy.css'))
		# Using flask-weasyprint to generate pdf ... facing foramtting issues here.
		return render_pdf(HTML(string=html_rendered), stylesheets=[stylesheet])

		
		# with open('exported_template.html', 'w') as f:
		# 	f.write(html_rendered)
		# command = "node pupeteer.js"
		# result = subprocess.run(command, shell=True, capture_output=True, text=True)
		# subprocess.Popen(["node", "pupeteer.js"])
		# return html_rendered		
	return render_template("front_end.html")

@app.route("/resume")
def hello_flask():
	print("this is printed from resume to the console...")
	with open("data.json", "r", encoding="utf8") as data:
		context = json.load(data)

	return render_template("flask_template.html",**context)



# context = {
# 	"work_experience" : [
# 			{
# 			"company_name":"Yog Enterprise Solutions",
# 			"place": "Indore, Madhya Pradesh",
# 			"designation":"Python Developer Intern",
# 			"period":"Jan 2024 - ",
# 			"work_description" : [
# 				"Working with Frappe/ERPNEXT framework to build reald world ERP applications for enterprises to solve business problems",
# 				"Domain Expertise: Learned about business processes and workflows to facilitate framework customization as per specific client requirements.",
# 				"Involved in Server Configuration and Management for organization.",
# 				"Added a job description here."
# 				]
# 			},
# 			{
# 			"company_name":"Company 2",
# 			"place": "place 2",
# 			"designation":"designation 2",
# 			"period":"period 2",
# 			"work_description" : [
# 				"point 1",
# 				"point 2",
# 				"point 3",
# 				"point 4"
# 				]
# 			}

# 		]
# 	}
	 
	