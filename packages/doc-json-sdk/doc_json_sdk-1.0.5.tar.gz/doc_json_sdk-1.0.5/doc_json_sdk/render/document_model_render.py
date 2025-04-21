# coding=UTF-8
import os
from typing import List, Dict

import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import pkg_resources
from doc_json_sdk.model.enums.layout_type_enum import LayoutTypeEnum

from doc_json_sdk.model.document_model import DocumentModel
from doc_json_sdk.model.base.pos_model import PosModel
from doc_json_sdk.model.doc.page_model import PageModel
from doc_json_sdk.model.layout.image.image_layout_model import ImageLayoutModel
from doc_json_sdk.model.layout.layout_model import LayoutModel
from doc_json_sdk.model.layout.paragraph.block import Block
from doc_json_sdk.model.layout.paragraph.paragraph_layout_model import ParagraphLayoutModel
from doc_json_sdk.model.layout.table.cell import Cell
from doc_json_sdk.model.layout.table.table_layout_model import TableLayoutModel
from doc_json_sdk.model.style.style_model import StyleModel
from doc_json_sdk.utils.log_util import log
from deepdiff import DeepDiff

# 渲染绘制
class DocumentModelRender:
    enable_text_block: bool = False
    enable_chat_block: bool = False
    document_model: DocumentModel
    __style_map: {int, StyleModel}

    def __init__(self, document_model: DocumentModel):
        self.document_model = document_model
        self.font_path = pkg_resources.resource_filename("doc_json_sdk", "fonts/PingFang.ttc")
        self.font = ImageFont.truetype(self.font_path)

    def render_image_result(self, output_dir: str, enable_text_block: bool = False,
                            enable_chat_block: bool = False):
        """

        draw doc-json result 绘制doc-json信息结果，目前支持视觉信息结果绘制

        -----------------------------------

            :param output_dir:
            :param output_path: 输出路径
            :param enable_text_block: 是否绘制文本块信息
            :param enable_chat_block: 是否绘制单字信息
        :return: void
        """
        os.makedirs(output_dir, exist_ok=True)
        self.enable_chat_block = enable_chat_block
        self.enable_text_block = enable_text_block
        for i in range(self.document_model.page_size):
            page_number: int = self.document_model.pages[i].get_page_id_cur_doc()
            result_image: np.ndarray = self._render_image_result(page_number)
            cv2.imwrite(os.path.join(output_dir, str(page_number) + '.png'), result_image)

    def render_markdown_result(self):
        md_result = ""
        for layout in self.document_model.layouts:
            type_enum = layout.get_layout_type_enum()
            if (type_enum == LayoutTypeEnum.Elements.FOOTER or
                    type_enum == LayoutTypeEnum.Elements.HEADER or
                    type_enum == LayoutTypeEnum.Elements.NOTE):
                # ignore header and footer notes
                continue
            elif type_enum == LayoutTypeEnum.Elements.IMAGE:
                if layout.type.find("_line")!=-1:
                    continue
                md_result += layout.markdownContent if layout.markdownContent!=None else layout.text
            elif type_enum == LayoutTypeEnum.Elements.TABLE:
                md_result += layout.markdownContent if layout.markdownContent!=None else layout.text
            else:
                md_result += layout.markdownContent if layout.markdownContent!=None else layout.text
            if md_result.endswith("\n") is False:
                md_result += "\n"
        return md_result

    def print_tree_title(self):
        tree = self._build_tree(self.document_model.layouts)
        self._print_directory_structure(tree)
        pass

    def _print_directory_structure(self,directory, prefix=''):
        items = list(directory.items())
        total_items = len(items)

        for i, (name, content) in enumerate(items):
            connector = '└── ' if i == total_items - 1 else '├── '
            print(prefix + connector + name)
            if isinstance(content, dict):
                next_prefix = prefix + ('    ' if i == total_items - 1 else '│   ')
                self._print_directory_structure(content, next_prefix)

    def _build_tree(self,layous):
        tree = {}
        stack = [(tree, -1)]  # (当前节点, 当前层级)

        for item in layous:
            if item.type.find("title")==-1:
                continue
            name = item.get_text()
            level = item.get_layout_level()

            # 创建新节点
            new_node = {}

            # 确保当前层级的正确性
            while stack and stack[-1][1] >= level:
                stack.pop()

            # 将新节点添加到当前节点
            stack[-1][0][name] = new_node

            # 添加当前节点到栈中
            stack.append((new_node, level))

        return tree

    def diff_other_document(self, compared_document: DocumentModel):
        def exclude_obj_callback(obj, path):
            if "pos" in path or "block" in path or "index" in path or "page_num" in path or "unique_id" in path:
                return True;
        def include_obj_callback(obj, path):
            if issubclass(type(obj), LayoutModel) or "layout" in path:
                return True
        diff = DeepDiff(self.document_model, compared_document,include_obj_callback=include_obj_callback,exclude_obj_callback=exclude_obj_callback)
        log.info(diff.pretty())
        return diff

    def _render_image_result(self, page_number: int) -> np.ndarray:
        """
        render page image with doc-mind results
        :param page_number:
        :return: np.ndarray
        """
        page_model: PageModel
        page_models = []
        for i in self.document_model.doc_info.get_pages():
            if i.get_page_id_cur_doc() == page_number:
                page_models.append(i)
        page_model = page_models[0]

        layouts = self.document_model.filter_layouts_by_page_number(page_number)

        self.__style_map = {}
        for i in self.document_model.styles:
            self.__style_map[i.get_style_id()] = i

        page_image_np = page_model.get_page_image()
        page_image = Image.fromarray(cv2.cvtColor(page_image_np.copy(), cv2.COLOR_BGR2RGB))
        text_image = Image.fromarray(cv2.cvtColor(np.ones(page_image_np.shape, np.uint8) * 255, cv2.COLOR_BGR2RGB))

        self.__draw_layout_info(layouts, ImageDraw.Draw(page_image), ImageDraw.Draw(text_image), page_number)
        page_image = cv2.cvtColor(np.asarray(page_image), cv2.COLOR_RGB2BGR)
        text_image = cv2.cvtColor(np.asarray(text_image), cv2.COLOR_RGB2BGR)
        result_image: np.ndarray = np.hstack((page_image, text_image))
        return result_image

    def __draw_layout_info(self, layouts: List[LayoutModel], graphics: ImageDraw, textgraphics: ImageDraw,
                           page_number: int):
        for i in layouts:
            pos = i.get_pos_model_by_page_number(page_number)
            color = "black"
            if isinstance(i, ParagraphLayoutModel):
                paragraph_layout_model: ParagraphLayoutModel = i
                color = "green"
                self.__draw_paragraph_model_info(paragraph_layout_model, graphics,
                                                 textgraphics)
            elif isinstance(i, TableLayoutModel):
                table_layout_model: TableLayoutModel = i
                color = "blue"
                self.__draw_table_model_info(table_layout_model, graphics, textgraphics,
                                             page_number)
            elif isinstance(i, ImageLayoutModel):
                color = "yellow"
            if len(pos) != 0:
                graphics.text([pos[0].get_x(), pos[0].get_y()], i.type, color)
                textgraphics.text([pos[0].get_x(), pos[0].get_y()], i.type, color)
                graphics.rectangle(xy=(pos[0].get_x(), pos[0].get_y(), pos[1].get_x(), pos[2].get_y()), width=2,
                                   outline=color)
                textgraphics.rectangle(xy=(pos[0].get_x(), pos[0].get_y(), pos[1].get_x(), pos[2].get_y()), width=2,
                                       outline=color)

    def __draw_paragraph_model_info(self, paragraph_layout_model: ParagraphLayoutModel, graphics: ImageDraw,
                                    textgraphics: ImageDraw):
        for block in paragraph_layout_model.get_blocks():
            self.__draw_block_info(block, graphics, textgraphics)
            if self.enable_text_block:
                graphics.rectangle(block.getPos(), width=2, outline=(120, 0, 255, 70))

    def __draw_block_info(self, block: Block, graphics: ImageDraw, textgraphics: ImageDraw):
        style: StyleModel = self.__style_map[block.get_style_id()]
        self.__cv2_add_chinese_text(img=textgraphics, text=block.get_text(),
                                    position=(block.get_pos()[0].get_x(), block.get_pos()[0].get_y()),
                                    text_color=(0, 0, 0), text_size=style.get_font_size() * 2)

    def __draw_table_model_info(self, table_layout_model: TableLayoutModel, graphics: ImageDraw,
                                textgraphics: ImageDraw, page_number: int):
        for cell in table_layout_model.get_cells():
            pos: list[PosModel] = cell.get_pos_model_by_page_number(page_number)
            if pos is None:
                continue
            graphics.rectangle(xy=(pos[0].get_x(), pos[0].get_y(), pos[2].get_x(), pos[2].get_y()), width=2,
                               outline=(0, 255, 0, 70))
            textgraphics.rectangle(xy=(pos[0].get_x(), pos[0].get_y(), pos[2].get_x(), pos[2].get_y()), width=2,
                                   outline=(0, 255, 0, 70))
            self.__draw_cell_info(cell, graphics, textgraphics, page_number)

    def __draw_cell_info(self, cell: Cell, graphics: ImageDraw, textgraphics: ImageDraw, page_number: int):
        if len(cell.get_layouts()) == 0:
            return

        for layout in cell.get_layouts():
            pos = layout.get_pos_model_by_page_number(page_number)
            graphics.rectangle(xy=(pos[0].get_x(), pos[0].get_y(), pos[1].get_x(), pos[2].get_y()), width=2,
                               outline=(0, 255, 0, 70))
            textgraphics.rectangle(xy=(pos[0].get_x(), pos[0].get_y(), pos[1].get_x(), pos[2].get_y()), width=2,
                                   outline=(0, 255, 0, 100))

            self.__cv2_add_chinese_text(img=textgraphics, text=layout.get_text(),
                                        position=(layout.get_min_x(), layout.get_min_y()),
                                        text_color=(0, 0, 0), text_size=20)

    def __cv2_add_chinese_text(self, img, text, position, text_color=(0, 255, 0), text_size=20):
        # 字体的格式
        font_style = ImageFont.truetype(self.font_path, text_size, encoding="utf-8")
        # 绘制文本
        img.text(position, text, text_color, font=font_style)
