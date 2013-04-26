#!/usr/bin/env python

# example helloworld.py

import pygtk
#pygtk.require('2.0')
import gtk
import Image
import string
import xml.etree.ElementTree as xml

mousePos = 0
ColourMap = "maps/testmap.png"
LoadMap = "maps/testmap.xml"
SaveMap = "maps/testmap.xml"



class Application:

    def new_province(self, widget, data=None):
        print "Creating New Province"
        if self.treeview.props.visible:
            self.oldMode = self.Mode
            self.Mode = "New Province"
            self.manage_buttons()
            self.showhide_interface("List")
            self.new_prov_col = "255 255 255"

            self.lbl_npName = gtk.Label("Province Name")
            self.fixed.put(self.lbl_npName,self.map.allocation.x+260,self.map.allocation.y)
            self.lbl_npName.show()

            self.txt_npName = gtk.Entry(50)
            self.fixed.put(self.txt_npName,self.map.allocation.x+350,self.map.allocation.y)
            self.txt_npName.show()

            self.lbl_npID = gtk.Label("New Prov Id:        "+str(self.provs_id_count))
            self.fixed.put(self.lbl_npID,self.map.allocation.x+260,self.map.allocation.y+32)
            self.lbl_npID.show()

            self.lbl_npCol = gtk.Label("Colour: "+str(self.new_prov_col))
            self.fixed.put(self.lbl_npCol,self.map.allocation.x+260,self.map.allocation.y+64)
            self.lbl_npCol.show()

            self.btn_npCol = gtk.Button("Pick Colour")
            self.fixed.put(self.btn_npCol,self.map.allocation.x+260+120,self.map.allocation.y+64)
            self.btn_npCol.set_size_request(75,20)
            self.btn_npCol.connect("clicked",self.get_colour_dialogue)
            self.btn_npCol.show()

            self.btn_npDone = gtk.Button("Add")
            self.fixed.put(self.btn_npDone,self.map.allocation.x+260,self.map.allocation.y+100)
            self.btn_npDone.set_size_request(75,35)
            self.btn_npDone.connect("clicked",self.list_update_province)
            self.btn_npDone.show()
        else:
            self.oldMode = self.Mode
            self.Mode = "Base"
            self.manage_buttons()
            self.showhide_interface("List")

    def list_update_province(self, widget):
        if (self.Mode == "New Province" and self.txt_npName.get_text() != "" and self.check_colour(self.new_prov_col)):
            self.btn_newProv.set_label("New Province")
            self.btn_edtProv.set_sensitive(True)
            self.provs.append(self.txt_npName.get_text())
            self.ls_provinces.append([self.provs[self.provs_id_count-1]])
            self.provs_rgb.append(self.new_prov_col)
            xy = string.split(self.get_prov_xy(self.new_prov_col))
            x = int(xy[0])
            y = int(xy[1])
            self.provs_x.append(x)
            self.provs_y.append(y)
            self.provs_id_count += 1

            self.oldMode = self.Mode
            self.Mode = "Base"
            self.manage_buttons()
            self.showhide_interface("List")
        elif (self.Mode == "Edit Province" and self.txt_epName.get_text() != "" and self.get_prov_xy(self.new_prov_col) != "Error"):
            self.btn_edtProv.set_label("Edit Province")
            self.btn_newProv.set_sensitive(True)
            self.provs[self.selected_prov] = self.txt_epName.get_text()
            #print str(self.ls_provinces[self.selected_prov-1][0])+" changes to "+self.provs[self.selected_prov]
            self.ls_provinces[self.selected_prov+1][0] = self.provs[self.selected_prov]
            self.provs_rgb[self.selected_prov] = self.new_prov_col
            xy = string.split(self.get_prov_xy(self.new_prov_col))
            x = int(xy[0])
            y = int(xy[1])
            self.provs_x.append(x)
            self.provs_y.append(y)

            self.oldMode = self.Mode
            self.Mode = "Base"
            self.manage_buttons()
            self.showhide_interface("List")
            self.treeview.set_cursor(0)
        else:
            msg = gtk.MessageDialog(self.window,
                gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR,
                gtk.BUTTONS_CLOSE, "You entered invalid data. Check the colour and name are both valid.")
            msg.run()
            msg.destroy()

    def edit_province(self, widget, data=None):
        if self.treeview.props.visible and self.selected_prov+1 > 0:
            self.oldMode = self.Mode
            self.Mode = "Edit Province"
            self.manage_buttons()
            self.new_prov_col = self.provs_rgb[self.selected_prov]
            self.showhide_interface("List")

            self.lbl_epName = gtk.Label("Province Name")
            self.fixed.put(self.lbl_epName,self.map.allocation.x+260,self.map.allocation.y)
            self.lbl_epName.show()

            self.txt_epName = gtk.Entry(80)
            self.fixed.put(self.txt_epName,self.map.allocation.x+350,self.map.allocation.y)
            self.txt_epName.set_text(self.provs[self.selected_prov])
            self.txt_epName.show()

            self.lbl_epID = gtk.Label("New Prov Id:        "+str(self.selected_prov+1))
            self.fixed.put(self.lbl_epID,self.map.allocation.x+260,self.map.allocation.y+32)
            self.lbl_epID.show()

            self.lbl_epCol = gtk.Label("Colour: "+str(self.new_prov_col))
            self.fixed.put(self.lbl_epCol,self.map.allocation.x+260,self.map.allocation.y+64)
            self.lbl_epCol.show()

            self.btn_epCol = gtk.Button("Change Colour")
            self.fixed.put(self.btn_epCol,self.map.allocation.x+260+120,self.map.allocation.y+64)
            self.btn_epCol.set_size_request(75,20)
            self.btn_epCol.connect("clicked",self.get_colour_dialogue)
            self.btn_epCol.show()

            self.btn_epDone = gtk.Button("Apply")
            self.fixed.put(self.btn_epDone,self.map.allocation.x+260,self.map.allocation.y+100)
            self.btn_epDone.set_size_request(75,35)
            self.btn_epDone.connect("clicked",self.list_update_province)
            self.btn_epDone.show()
        elif self.Mode == "Edit Province":
            self.oldMode = self.Mode
            self.Mode = "Base"
            self.manage_buttons()
            self.showhide_interface("List")

    def delete_province(self, widget, data=None):
        if self.selected_prov>-1:
            ques = gtk.MessageDialog(self.window,
                gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION,
                gtk.BUTTONS_YES_NO, "Are you sure you want to delete "+self.provs[self.selected_prov]+"?")
            response = ques.run()
            treeselection = self.treeview.get_selection()
            (model, iter) = treeselection.get_selected()
            print response
            if response == -8 and iter != None: # a YES response
                del self.provs[self.selected_prov]
                del self.provs_x[self.selected_prov]
                del self.provs_y[self.selected_prov]
                del self.provs_rgb[self.selected_prov]
                self.provs_id_count -= 1
                print model, iter
                self.ls_provinces.remove(iter)
            ques.destroy()

    def get_colour_dialogue(self, widget):
        self.oldMode = self.Mode
        self.Mode = "Pick Colour"
        self.manage_buttons()

    def check_colour(self,colour):
        result = True
        if colour != "0 0 0" and colour != "255 255 255":
            for p in range(len(self.provs_rgb)):
                if (self.provs_rgb[p] == colour):
                    if p == self.selected_prov and self.oldMode == "Edit Province":
                        print "THAT ME! My colour is: "+self.provs_rgb[p]+" and you chose "+colour
                    else:
                        print "You dirty bastard! That's someone else's colour! "+self.provs_rgb[p]+" doesn't belong to me! You chose "+colour
                        result = False
        else:
            result = False
        return result

    def global_click(self, window, widget):
        #self.lbl_npCol.set_markup("<span color='#00FF00'>Choosing Colour</span>")
        print "global click"
        if self.Mode == "Pick Colour":
            if (self.mouse_x > self.map.allocation.x and self.mouse_x < self.map.allocation.x+256 and
                    self.mouse_y > self.map.allocation.y and self.mouse_y < self.map.allocation.y+256):
                img_x = self.mouse_x - self.map.allocation.x
                img_y = self.mouse_y - self.map.allocation.y
                new_colour = self.convert_col_to_str(self.map_pixels[img_x,img_y])

                if (self.check_colour(new_colour)):
                    self.new_prov_col = new_colour
                else:
                    msg = gtk.MessageDialog(self.window,
                        gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR,
                        gtk.BUTTONS_CLOSE, "Invalid Colour. It is either already in use, ocean, or a city pixel.")
                    msg.run()
                    msg.destroy()
                    if (self.oldMode == "New Province"):
                        self.lbl_npCol.set_text("Colour: "+str(self.new_prov_col))
                    elif (self.oldMode == "Edit Province"):
                        self.lbl_epCol.set_text("Colour: "+str(self.new_prov_col))
            if (self.oldMode == "New Province"):
                self.lbl_npCol.set_text("Colour: "+str(self.new_prov_col))
            elif (self.oldMode == "Edit Province"):
                self.lbl_epCol.set_text("Colour: "+str(self.new_prov_col))
            self.manage_buttons()
            self.Mode = self.oldMode
            self.oldMode = "Pick Colour"

        if self.Mode == "Base":
            if (self.mouse_x > self.map.allocation.x and self.mouse_x < self.map.allocation.x+256):
                if (self.mouse_y > self.map.allocation.y and self.mouse_y < self.map.allocation.y+256):
                    img_x = self.mouse_x - self.map.allocation.x
                    img_y = self.mouse_y - self.map.allocation.y
                    prov_col = self.map_pixels[img_x,img_y]

                    if prov_col != (255,255,255,255) and prov_col != (0,0,0,255):
                        prov_col = self.convert_col_to_str(prov_col)
                        prov_id = self.find_colour_id(prov_col)

                        if prov_id != -1:
                            self.treeview.set_cursor(prov_id)
                        else:
                            self.treeview.set_cursor(0)
                    else:
                        self.treeview.set_cursor(0)

    def convert_col_to_str(self,colour):
        print "prov_col "+str(colour)
        colour = str(colour)
        colour = string.replace(colour,"(","")
        colour = string.replace(colour,")","")
        colour = string.replace(colour,", "," ")

        split_col = string.split(colour)
        colour = split_col[0]+" "+split_col[1]+" "+split_col[2]

        print "new prov_col "+colour
        return colour

    def manage_buttons(self):
        if self.Mode == "New Province":
            self.btn_newProv.set_label("Cancel")
            self.btn_edtProv.set_sensitive(False)
            self.btn_delProv.set_sensitive(False)
            self.btn_sveMap.set_sensitive(False)
        elif self.Mode != "Pick Colour" and self.oldMode == "New Province":
            self.btn_newProv.set_label("New Province")
            self.btn_edtProv.set_sensitive(True)
            self.btn_delProv.set_sensitive(True)
            self.btn_sveMap.set_sensitive(True)
            self.lbl_npName.destroy()
            self.txt_npName.destroy()
            self.lbl_npID.destroy()
            self.lbl_npCol.destroy()
            self.btn_npCol.destroy()
            self.btn_npDone.destroy()
        elif self.Mode == "Edit Province":
            self.btn_edtProv.set_label("Cancel")
            self.btn_newProv.set_sensitive(False)
            self.btn_delProv.set_sensitive(False)
            self.btn_sveMap.set_sensitive(False)
        elif self.Mode != "Pick Colour" and self.oldMode == "Edit Province":
            self.btn_edtProv.set_label("Edit Province")
            self.btn_newProv.set_sensitive(True)
            self.btn_delProv.set_sensitive(True)
            self.btn_sveMap.set_sensitive(True)
            self.lbl_epName.destroy()
            self.txt_epName.destroy()
            self.lbl_epID.destroy()
            self.lbl_epCol.destroy()
            self.btn_epCol.destroy()
            self.btn_epDone.destroy()
        elif self.Mode == "Pick Colour" and self.oldMode == "New Province":
            if (self.txt_npName.get_sensitive()):
                self.btn_newProv.set_sensitive(False)
                self.btn_npCol.set_sensitive(False)
                self.txt_npName.set_sensitive(False)
                self.btn_npDone.set_sensitive(False)
                self.lbl_npCol.set_markup("<span color='#00FF00'>Choosing Colour</span>")
            else:
                self.btn_newProv.set_sensitive(True)
                self.btn_npCol.set_sensitive(True)
                self.txt_npName.set_sensitive(True)
                self.btn_npDone.set_sensitive(True)
        elif self.Mode == "Pick Colour" and self.oldMode == "Edit Province":
            if (self.txt_epName.get_sensitive()):
                self.btn_edtProv.set_sensitive(False)
                self.btn_epCol.set_sensitive(False)
                self.txt_epName.set_sensitive(False)
                self.btn_epDone.set_sensitive(False)
                self.lbl_epCol.set_markup("<span color='#00FF00'>Choosing Colour</span>")
            else:
                self.btn_edtProv.set_sensitive(True)
                self.btn_epCol.set_sensitive(True)
                self.txt_epName.set_sensitive(True)
                self.btn_epDone.set_sensitive(True)

    def showhide_interface(self,intfce):
        if intfce == "List":
            if self.treeview.props.visible:
                self.treeview.hide()
                self.lbl_prvDtls.hide()
                self.lbl_prvName.hide()
                self.lbl_prvID.hide()
                self.lbl_prvXY.hide()
                self.lbl_prvCol.hide()
            else:
                self.treeview.show()
                self.lbl_prvDtls.show()
                self.lbl_prvName.show()
                self.lbl_prvID.show()
                self.lbl_prvXY.show()
                self.lbl_prvCol.show()

    def get_province_tag(self, prov_id, prov_tag):
        prov = self.root.find('.//province[@id="'+str(prov_id)+'"]')
        tag = prov.find(prov_tag).text
        return tag

    def load_map_data(self, map_file):
        tree = xml.parse(map_file)
        self.root = tree.getroot()

        self.provs = []
        self.provs_x = []
        self.provs_y = []
        self.provs_rgb = []
        self.provs_id_count = 1

        counter = 1
        for p in self.root.findall("province"):
            self.provs.append(self.get_province_tag(counter, "name"))
            self.provs_x.append(self.get_province_tag(counter, "x"))
            self.provs_y.append(self.get_province_tag(counter, "y"))
            self.provs_rgb.append(self.get_province_tag(counter, "rgb"))
            print self.provs[counter-1], self.provs_x[counter-1], self.provs_y[counter-1],self.provs_rgb[counter-1]
            counter+=1
            self.provs_id_count = counter

    def get_prov_xy(self, col):
        found = False
        for x in range(self.im_width):
            for y in range(self.im_height):
                if self.map_pixels[x,y] == (0, 0, 0, 255):
                    print "BLACK DOT"
                    pc = col
                    pc = string.split(col)
                    prov_col = "("+pc[0]+", "+pc[1]+", "+pc[2]+", 255)"

                    if str(self.map_pixels[x-1,y]) == prov_col:
                        found = True
                        return(str(x)+" "+str(y))
                        break
        if found == False:
            return "Error"

    def load_map_colour(self, map_file):
        im = Image.open(map_file)
        self.map_pixels = im.load()

        self.im_width, self.im_height = im.size
        for x in range(self.im_width):
            for y in range(self.im_height):
                if self.map_pixels[x,y] == (0, 0, 0, 255):
                    for p in range(len(self.provs_rgb)):
                        prov_col = str(self.provs_rgb[p])
                        col = string.split(prov_col)
                        prov_col = "("+col[0]+", "+col[1]+", "+col[2]+", 255)"

                        if str(self.map_pixels[x-1,y]) == prov_col:
                            self.provs_x[p] = x
                            self.provs_y[p] = y

    def find_colour_prov(self, colour):
        value = "\n\n<span color='#FF0000'>Unassigned</span>"
        for p in range(len(self.provs_rgb)):
            prov_col = str(self.provs_rgb[p])
            col = string.split(prov_col)
            prov_col = "("+col[0]+", "+col[1]+", "+col[2]+", 255)"
            if prov_col == str(colour):
                value = "\n\n"+self.provs[p]
                break
        return value

    def find_colour_id(self, given_col):
        return_id = -1
        for p in range(len(self.provs_rgb)):
            if given_col == self.provs_rgb[p]:
                return_id = p+1
        return return_id

    def mouse_checks(self, window, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        if (event.x > self.map.allocation.x and event.x < self.map.allocation.x+256):
            if (event.y > self.map.allocation.y and event.y < self.map.allocation.y+256):
                img_x = event.x - self.map.allocation.x
                img_y = event.y - self.map.allocation.y
                if (self.map_pixels[img_x, img_y] != (255,255,255,255)):
                    self.lbl_colXY.set_text(str(img_x)+","+str(img_y))
                    self.lbl_colDetail.set_text("\n"+str(self.map_pixels[img_x,img_y]))
                    self.lbl_colTown.set_markup(self.find_colour_prov(self.map_pixels[img_x, img_y]))
                else:
                    self.lbl_colXY.set_text(str(img_x)+","+str(img_y))
                    self.lbl_colDetail.set_text("\nWhite Space")
                    self.lbl_colTown.set_markup("\n\n<span color='#2222FF'>Ocean</span>")

    def draw_interface(self):
        self.fixed = gtk.Fixed()
        self.window.add(self.fixed)
        self.fixed.show()

        self.window.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.window.connect('motion-notify-event', self.mouse_checks)
        self.window.connect('destroy', lambda w: gtk.main_quit())
        #self.window.show_all()
        self.map = gtk.image_new_from_file(ColourMap)
        mp = self.fixed.put(self.map,20,20)
        self.imgOverlay = -1

        self.map.show()

        self.window.show()

    def create_list_provinces(self):
        self.ls_provinces = gtk.ListStore(str)
        self.treeview = gtk.TreeView(self.ls_provinces)
        self.ls_provinces.append(["<None>"])
        for p in range(len(self.provs)):
            self.ls_provinces.append([self.provs[p]])

        column = gtk.TreeViewColumn("Provinces")
        self.treeview.append_column(column)

        cell = gtk.CellRendererText()
        column.pack_start(cell, False)
        column.add_attribute(cell, "text",0)
        column.set_min_width(120)

        tree_selection = self.treeview.get_selection()
        tree_selection.connect("changed", self.update_prov_details)

        self.fixed.put(self.treeview,self.map.allocation.x+270,self.map.allocation.y)

        self.treeview.show()

        self.lbl_prvName = gtk.Label("")
        self.fixed.put(self.lbl_prvName,self.map.allocation.x+270+120+2,self.map.allocation.y)
        self.lbl_prvName.set_markup("<span size='20000' foreground='#FF0000'>"+"No Province Chosen"+"</span>")
        self.lbl_prvName.show()

        self.lbl_prvDtls = gtk.Label("")
        self.fixed.put(self.lbl_prvDtls,self.map.allocation.x+270+120+2,self.map.allocation.y+40)
        self.lbl_prvDtls.set_markup("<span>ID:\nXY:\nColour:\n</span>")
        self.lbl_prvDtls.show()

        self.lbl_prvID = gtk.Label("")
        self.fixed.put(self.lbl_prvID,self.map.allocation.x+270+120+2+128,self.map.allocation.y+40)
        self.lbl_prvID.set_markup("<span foreground='#FF0000'>-1</span>")
        self.lbl_prvID.show()

        self.lbl_prvXY = gtk.Label("")
        self.fixed.put(self.lbl_prvXY,self.map.allocation.x+270+120+2+128,self.map.allocation.y+40)
        self.lbl_prvXY.set_markup("\n<span foreground='#FF0000'>-1,-1</span>")
        self.lbl_prvXY.show()

        self.lbl_prvCol = gtk.Label("")
        self.lbl_prvCol.set_use_markup(True)
        self.fixed.put(self.lbl_prvCol,self.map.allocation.x+270+120+2+128,self.map.allocation.y+40)
        self.lbl_prvCol.set_markup("\n\n<span foreground='#FF0000'>(-1,-1,-1,-1)</span>")
        self.lbl_prvCol.show()

        print str(self.ls_provinces[1][0]),str(self.ls_provinces[2][0]),str(self.ls_provinces[3][0]),str(self.ls_provinces[4][0])

    def update_prov_details(self, selection):
        (model, pathlist) = selection.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter,0)
            prov_id = str(path)
            prov_id = string.replace(prov_id,"(","")
            prov_id = string.replace(prov_id,",","")
            prov_id = string.replace(prov_id,")","")
            prov_id = int(prov_id)
            self.selected_prov = prov_id-1
            #print self.selected_prov
            print value, str(prov_id)
            if int(prov_id) > 0:
                self.lbl_prvName.set_markup("<span size='20000' foreground='#000000'>"+self.provs[prov_id-1]+"</span>")
                self.lbl_prvID.set_markup("<span foreground='#000000'>"+str(prov_id)+"</span>")
                self.lbl_prvXY.set_markup("\n<span foreground='#000000'>"+str(self.provs_x[prov_id-1])+","+str(self.provs_y[prov_id-1])+"</span>")
                self.lbl_prvCol.set_markup("\n\n<span foreground='#000000'>"+str(self.provs_rgb[prov_id-1])+"</span>")
                self.draw_prov_focus(self.provs_rgb[prov_id-1])
            else:
                self.lbl_prvName.set_markup("<span size='20000' foreground='#FF0000'>(None Selected)</span>")
                self.lbl_prvID.set_markup("<span foreground='#FF0000'>(Unidentified)</span>")
                self.lbl_prvXY.set_markup("\n<span foreground='#FF0000'>(Nowhere)</span>")
                self.lbl_prvCol.set_markup("\n\n<span foreground='#FF0000'>(None)</span>")
                if self.imgOverlay != -1:
                    self.imgOverlay.destroy()
                    self.imgOverlay = -1

    def draw_prov_focus(self, prov_col):
        filename = "maps/overlay.png"
        overlay = Image.new("RGBA",(256,256),(0,0,0,100))
        o_pixels = overlay.load()
        col = string.split(prov_col)
        given_col = "("+col[0]+", "+col[1]+", "+col[2]+", 255)"
        print given_col
        for x in range(overlay.size[0]):
            for y in range(overlay.size[1]):
                if str(self.map_pixels[x,y]) == given_col:
                    #print "CHANGE COLOUR" + str(o_pixels[x,y])+" to "+str(self.map_pixels[x,y])
                    o_pixels[x,y] = (int(col[0]),int(col[1]),int(col[2]),255)
        overlay.save(filename)
        #self.imgOverlay.set_from_file("overlay.png")
        if self.imgOverlay == -1:
            self.imgOverlay = gtk.image_new_from_file(filename)
            imgO = self.fixed.put(self.imgOverlay,20,20)
            self.imgOverlay.show()
        else:
            self.imgOverlay.set_from_file(filename)

    def add_tag(self, elem,name,text):
        tag = xml.SubElement(elem, name)
        if text != "":
            tag.text = str(text)

    def add_province(self, root, prov_id, prov_name, prov_x, prov_y ,prov_rgb):
        province = xml.Element("province")
        province.attrib["id"] = str(prov_id)
        root.append(province)
        self.add_tag(province, "name", prov_name)
        self.add_tag(province, "x", prov_x)
        self.add_tag(province, "y", prov_y)
        self.add_tag(province, "rgb", prov_rgb)

    def save_map(self, widget):
        root = xml.Element("WorldMap")

        for i in range(len(self.provs)):
            self.add_province(root, i+1, self.provs[i],self.provs_x[i], self.provs_y[i],self.provs_rgb[i])

        file = open(SaveMap, 'w')
        xml.ElementTree(root).write(file)
        file.close()

    def draw_buttons(self):
        self.btn_sveMap = gtk.Button("Save Map")
        self.btn_sveMap.set_size_request(80,30)
        self.btn_sveMap.set_tooltip_text("Save this data to XML")
        self.btn_sveMap.connect("clicked",self.save_map)#gtk.main_quit
        self.fixed.put(self.btn_sveMap,self.map.allocation.x,self.map.allocation.y+256+50)
        self.btn_sveMap.show()

        self.btn_newProv = gtk.Button("New Province")
        self.btn_newProv.set_size_request(95,30)
        self.btn_newProv.set_tooltip_text("Create a new province and assign it to a colour")
        self.btn_newProv.connect("clicked",self.new_province)#gtk.main_quit
        self.fixed.put(self.btn_newProv,self.map.allocation.x+256+400,self.map.allocation.y)
        self.btn_newProv.show()

        self.btn_edtProv = gtk.Button("Edit Province")
        self.btn_edtProv.set_size_request(95,30)
        self.btn_edtProv.set_tooltip_text("Change the properties of selected province")
        self.btn_edtProv.connect("clicked",self.edit_province)#gtk.main_quit
        self.fixed.put(self.btn_edtProv,self.map.allocation.x+256+400,self.map.allocation.y+40)
        self.btn_edtProv.show()

        self.btn_delProv = gtk.Button("Delete Province")
        self.btn_delProv.set_size_request(95,30)
        self.btn_delProv.set_tooltip_text("Completely delete a province")
        self.btn_delProv.connect("clicked",self.delete_province)#gtk.main_quit
        self.fixed.put(self.btn_delProv,self.map.allocation.x+256+400,self.map.allocation.y+80)
        self.btn_delProv.show()

    def draw_labels(self):
        self.lbl_tags = gtk.Label("XY:\nColour & Alpha:\nProvince:")
        self.fixed.put(self.lbl_tags,self.map.allocation.x,self.map.allocation.y+256)
        self.lbl_tags.show()

        self.lbl_colXY = gtk.Label("")
        self.lbl_colXY.set_alignment(1.0,-1.0)
        self.fixed.put(self.lbl_colXY,self.map.allocation.x,self.map.allocation.y+256)
        self.lbl_colXY.set_size_request(256,50)

        self.lbl_colDetail = gtk.Label("")
        self.lbl_colDetail.set_alignment(1.0,-1.0)
        self.fixed.put(self.lbl_colDetail,self.map.allocation.x,self.map.allocation.y+256)
        self.lbl_colDetail.set_size_request(256,50)

        self.lbl_colTown = gtk.Label("\n\n")
        self.lbl_colTown.set_alignment(1.0,-1.0)
        self.fixed.put(self.lbl_colTown,self.map.allocation.x,self.map.allocation.y+256)
        self.lbl_colTown.set_size_request(256,80)

        self.create_list_provinces()

        self.lbl_colDetail.show()
        self.lbl_colTown.show()
        self.lbl_colXY.show()

    def __init__(self):
        self.Mode = "Base"
        self.selected_prov = -1

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("World Map Region Editor")
        self.window.set_size_request(800,600)
        self.window.connect("delete_event",gtk.main_quit)
        self.window.connect("button-press-event", self.global_click)

        self.window.add_events(gtk.gdk.BUTTON_PRESS_MASK)

        self.load_map_data(LoadMap)
        self.load_map_colour(ColourMap)


        self.draw_interface()
        self.draw_labels()
        self.draw_buttons()

    def main(self):
        gtk.main()
if __name__ == "__main__":
    app = Application()
    app.main()