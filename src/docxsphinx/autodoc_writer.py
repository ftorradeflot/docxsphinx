
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

PAR_INDENT_PT = 30

class ClassWriter():

    def __init__(self, translator, node):

        self.translator = translator
        self.parent_node = node
        self.desc_signature, self.desc_content = self.get_children_nodes_from_types(self.parent_node, \
            ['desc_signature', 'desc_content'])

    def get_children_nodes_from_types(self, parent_node, types_list):
        
        children_nodes = []
        for node_type in types_list:
            chosen_node = None
            for child_node in parent_node.children:
                if child_node.tagname == node_type:
                    chosen_node = child_node
                    break
            children_nodes.append(chosen_node)
        return(children_nodes)

    def write(self):
        
        self.write_main(self.desc_signature, self.desc_content)
        self.write_class_content()

    def write_main(self, desc_signature, desc_content, curr_indent=0):
        
        #self.translator.current_paragraph.paragraph_format.space_before = Pt(10)
        desc_annotation = ''
        desc_module = ''
        desc_name = ''
        desc_parameter_list = ''
        for node in desc_signature.children:
            if node.tagname == 'desc_annotation':
                desc_annotation = node.astext()
            elif node.tagname == 'desc_addname':
                desc_module = node.astext()
            elif node.tagname == 'desc_name':
                desc_name = node.astext()
            elif node.tagname == 'desc_parameterlist':
                desc_parameter_list = node
    
        class_arg_text = ', '.join([node.astext() for node in desc_parameter_list])
        class_main_text = desc_annotation + desc_module + desc_name
        class_main_text += '(' + class_arg_text + ')' 
        #self.translator.strong = True
        p = self.translator.current_state.location.add_paragraph() #class_main_text)
        r = p.add_run(class_main_text)
        r.bold = True
        p.paragraph_format.left_indent = Pt(curr_indent)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(0)
        self.translator.current_paragraph = p
        #self.translator.strong = False
        
        for nodes in desc_content.children:
            if nodes.tagname == 'paragraph':
                p = self.translator.current_state.location.add_paragraph(nodes.astext())
                p.paragraph_format.left_indent = Pt(curr_indent + PAR_INDENT_PT)
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
                self.translator.current_paragraph = p
                #self.translator.current_state.location = p
               
    def write_class_content(self):
        
        curr_indent = self.translator.current_paragraph.paragraph_format.left_indent
        curr_indent = curr_indent and curr_indent.pt or 0
        
        for node in self.desc_content.children:
            #self.translator.add_text(str(node.children))
            #self.translator.add_text(node.tagname + ', ' + node.astext())
            if node.tagname == 'desc':
                desc_signature, desc_content = self.get_children_nodes_from_types(node, \
                    ['desc_signature', 'desc_content'])
                self.write_main(desc_signature, desc_content, curr_indent)
                
                definition_list, = self.get_children_nodes_from_types(desc_content,
                                                                      ['definition_list'])
                if definition_list: self.write_definition_list(definition_list)
                    
    def write_definition_list(self, definition_list_node):
        
        curr_loc = self.translator.current_state.location
        curr_indent = self.translator.current_paragraph.paragraph_format.left_indent
        curr_indent = curr_indent and curr_indent.pt or 0
        
        for definition_list_item in definition_list_node.children:
            #self.translator.add_text(definition_list_item.tagname + ', ' + definition_list_item.astext())
            #self.translator.add_text(str(definition_list_item.children))
            
            term, classifier, definition = self.get_children_nodes_from_types(definition_list_item,
                ['term', 'classifier', 'definition'])
            
            p = curr_loc.add_paragraph(term.astext() + ' : ' + classifier.astext())            
            p.paragraph_format.left_indent = Pt(curr_indent)
            p.paragraph_format.space_after = Pt(0)
            
            p = curr_loc.add_paragraph(definition.astext())
            p.paragraph_format.left_indent = Pt(curr_indent + PAR_INDENT_PT)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            #self.translator.current_paragraph = p
                
                 