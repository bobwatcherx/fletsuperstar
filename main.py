from flet import *
from pocketbase import PocketBase  # Client also works the same

client = PocketBase('https://gigantic-kitchen.pockethost.io/')

class MyBook(UserControl):
	def __init__(self):
		super().__init__()
		self.listbook = Column(scroll=True,visible=True)
		self.ctinput = Container(
			visible=False,
			bgcolor="red200",
			padding=10,
				content=Column([
					Row([
						Text("Books Library",size=30,weight="bold"),
					IconButton(icon="close",icon_color="red",
							on_click=self.closeinput
							)
					]),
					TextField(label="Book name"),
					TextField(label="Image Url Books"),
					TextField(label="years"),
					TextField(label="Pages"),
					TextField(label="Author"),
					TextField(label="Description"),
					TextField(label="Email"),
					Row([
						ElevatedButton("add Books",
							bgcolor="blue",color="white",
							on_click=self.addbooks
							),
						ElevatedButton("Delete This",
							bgcolor="red",color="white",
							visible=False,
							on_click=self.deletebooks
							)
						],alignment="center"),
					Text(visible=False)
					]),
				)

	def clearinput(self):
		self.ctinput.content.controls[1].value = ""
		self.ctinput.content.controls[2].value = ""
		self.ctinput.content.controls[3].value = ""
		self.ctinput.content.controls[4].value = ""
		self.ctinput.content.controls[5].value = ""
		self.ctinput.content.controls[6].value = ""
		self.ctinput.content.controls[7].value =""
		self.ctinput.content.controls[9].value =""

		self.page.update()

	def loguser(self):
		user_data = client.collection("users").auth_with_password(
    "mio@gmail.com", "qwerty123")

	def deletebooks(self,e):
		idupdate = self.ctinput.content.controls[9].value
		try:
			self.loguser()
			client.collection("books_col").delete(idupdate)
			self.page.snack_bar = SnackBar(
				content=Text("Success Delete",size=30,color="white"),
				bgcolor="blue"
				)
			self.page.snack_bar.open = True
			self.ctinput.visible = False
			self.listbook.visible = True
			self.getallboks()
			self.clearinput()

			self.page.update()
		except Exception as e:
			print(e)
			self.page.snack_bar = SnackBar(
				content=Text(e,size=30,color="white"),
				bgcolor="red"
				)
			self.page.snack_bar.open = True
			self.page.update()	



	def getallboks(self):
		self.listbook.controls.clear()
		try:
			self.loguser()
			getbok = client.collection("books_col").get_list()
			print(getbok)
			for x in getbok.items:
				self.listbook.controls.append(
				ListTile(
					leading=CircleAvatar(
						foreground_image_url=x.collection_id['image']
						),
					title=Row([
						Text(x.collection_id['books_name'],
							weight="bold",size=20
							),
						
						]),
					subtitle=Column([
						Row([
						Text(f"years :{x.collection_id['years']}",weight="bold"),
						Text(f"pages : {x.collection_id['pages']}",weight="bold"),
						],alignment="spaceBetween"),
						Row([
						Text(f"Author :{x.collection_id['author']}",weight="bold"),
						],alignment="start"),
						Row([
						Text(f"{x.collection_id['description']}"),
						],wrap=True),
						]),
					data=x.collection_id,
					on_click=self.willupdate
					)
				)
			self.update()

		except Exception as e:
			print(e)

		self.update()



	def willupdate(self,e):
		data = e.control.data
		self.showaddnewbook(e)

		print(data)
		self.ctinput.content.controls[1].value = data['books_name']
		self.ctinput.content.controls[2].value = data['image']
		self.ctinput.content.controls[3].value = data['years']
		self.ctinput.content.controls[4].value = data['pages']
		self.ctinput.content.controls[5].value = data['author']
		self.ctinput.content.controls[6].value = data['description']
		self.ctinput.content.controls[7].value = data['email']
		self.ctinput.content.controls[8].controls[0].text = "Update Data"
		self.ctinput.content.controls[8].controls[0].on_click = self.editdata
		

		# ENABLE DELETE
		self.ctinput.content.controls[8].controls[1].visible = True

		self.ctinput.content.controls[0].controls[0].value = "Update Data"
		self.ctinput.content.controls[9].value = data['id']
		
		self.ctinput.bgcolor = "green200"

		self.update()


	def editdata(self,e):
		idupdate = self.ctinput.content.controls[9].value
		data = {
		  "books_name": self.ctinput.content.controls[1].value,
	    "image": self.ctinput.content.controls[2].value,
	    "years": self.ctinput.content.controls[3].value,
	    "pages": self.ctinput.content.controls[4].value,
	    "author": self.ctinput.content.controls[5].value,
	    "description": self.ctinput.content.controls[6].value,
	    "email": self.ctinput.content.controls[7].value
		}
		try:
			self.loguser()
			client.collection("books_col").update(idupdate,data)
			self.page.snack_bar = SnackBar(
				content=Text("Success Edit",size=30,color="white"),
				bgcolor="blue"
				)
			self.page.snack_bar.open = True
			self.ctinput.visible = False
			self.listbook.visible = True
			self.getallboks()
			self.clearinput()

			self.page.update()
		except Exception as e:
			print(e)
			self.page.snack_bar = SnackBar(
				content=Text(e,size=30,color="white"),
				bgcolor="red"
				)
			self.page.snack_bar.open = True
			self.page.update()	





	def addbooks(self,e):
		data = {
		  "books_name": self.ctinput.content.controls[1].value,
	    "image": self.ctinput.content.controls[2].value,
	    "years": self.ctinput.content.controls[3].value,
	    "pages": self.ctinput.content.controls[4].value,
	    "author": self.ctinput.content.controls[5].value,
	    "description": self.ctinput.content.controls[6].value,
	    "email": self.ctinput.content.controls[7].value
		}
		try:
			self.loguser()
			client.collection("books_col").create(data)
			self.page.snack_bar = SnackBar(
				content=Text("Success add",size=30,color="white"),
				bgcolor="green"
				)
			self.page.snack_bar.open = True
			self.ctinput.visible = False
			self.listbook.visible = True
			self.getallboks()
			self.clearinput()
			self.page.update()
		except Exception as e:
			print(e)
			self.page.snack_bar = SnackBar(
				content=Text(e,size=30,color="white"),
				bgcolor="red"
				)
			self.page.snack_bar.open = True
			self.page.update()

	def did_mount(self):
		self.getallboks()

	def showaddnewbook(self,e):
		self.listbook.visible = False
		self.ctinput.visible = True
		self.ctinput.bgcolor = "red200"
		self.ctinput.content.controls[8].controls[0].text = "add Data"
		self.ctinput.content.controls[8].controls[0].on_click = self.addbooks
		self.ctinput.content.controls[8].controls[1].visible = False
		self.clearinput()
		self.update()
	def closeinput(self,e):
		self.listbook.visible = True
		self.ctinput.visible = False
		self.ctinput.bgcolor = "red200"
		self.ctinput.content.controls[8].controls[0].text = "add Data"
		self.ctinput.content.controls[8].controls[0].on_click = self.addbooks
		self.ctinput.content.controls[8].controls[1].visible = False
		self.clearinput()

		self.update()

	def build(self):
		return Column([
			Row([
				Text("books System",size=25,weight="bold"),
				ElevatedButton("add new books",
					bgcolor="blue",color="white",
					on_click=self.showaddnewbook
					)
				],alignment="end"),
			self.listbook,
			self.ctinput
			])




def main(page:Page):
	page.window_width=350
	page.scroll = True
	mybook = MyBook()
	page.add(
		mybook
		)

flet.app(target=main)
