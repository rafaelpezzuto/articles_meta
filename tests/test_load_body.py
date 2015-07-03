# coding: utf-8
import unittest
import os
import codecs

from processing import load_body

class LoadLicensesTest(unittest.TestCase):

    def test_scrapt_body(self):

        data = u"""<html><header></header><body><div class="content"><div class="index,en"><div class="title">Crazy <i>Title</i></div><p>Crazy Body</p><p>Really Crazy Body</p></div></div></body></html>"""

        result = load_body.scrap_body(data, 'en')

        self.assertEqual(result, '<div class="title">Crazy <i>Title</i></div><p>Crazy Body</p><p>Really Crazy Body</p>')

    def test_regex_remove_links(self):
      import re

      data = """<p>ref 1: [ <a href="javascript:void(0);" onclick="javascript: window.open('/scielo.php?script=sci_nlinks&amp;ref=000129&amp;pid=S0001-3765200400030001400030&amp;lng=pt','','width=640,height=500,resizable=yes,scrollbars=1,menubar=yes,');">Links</a> ]</p><p>ref 2:    [ <a href="javascript:void(0);" onclick="javascript: window.open('/scielo.php?script=sci_nlinks&amp;ref=000129&amp;pid=S0001-3765200400030001400030&amp;lng=pt','','width=640,height=500,resizable=yes,scrollbars=1,menubar=yes,');">Links</a> ]</p>"""

      result = load_body.REMOVE_LINKS_REGEX.sub(' ', data, count=0)

      self.assertEqual(result, '<p>ref 1:  </p><p>ref 2:     </p>')


    def test_regex_remove_links_ignore_case(self):
      import re

      data = """<p>ref 1: [ <a href="javascript:void(0);" onclick="javascript: window.open('/scielo.php?script=sci_nlinks&amp;ref=000129&amp;pid=S0001-3765200400030001400030&amp;lng=pt','','width=640,height=500,resizable=yes,scrollbars=1,menubar=yes,');">Links</a> ]</p><p>ref 2:    [ <a href="javascript:void(0);" onclick="javascript: window.open('/scielo.php?script=sci_nlinks&amp;ref=000129&amp;pid=S0001-3765200400030001400030&amp;lng=pt','','width=640,height=500,resizable=yes,scrollbars=1,menubar=yes,');">links</a> ]</p>"""

      result = load_body.REMOVE_LINKS_REGEX.sub(' ', data, count=0)

      self.assertEqual(result, '<p>ref 1:  </p><p>ref 2:     </p>')

    def test_scrapt_body_line_breaked(self):

        data = u"""
          <html>
            <header></header>
            <body>
              <div class="content">
                <div class="index,en">
                  <div class="title">Crazy <i>Title</i></div>
                  <p>Crazy Body</p>
                  <p>Really Crazy Body</p>
                </div>
              </div>
            </body>
          </html>
          """

        result = load_body.scrap_body(data, 'en')

        self.assertEqual(result, '<div class="title">Crazy <i>Title</i></div> <p>Crazy Body</p> <p>Really Crazy Body</p>')

    def test_scrapt_body_not_found_for_a_given_language(self):

        data = u"""<html><header></header><body><div class="content"><div class="index,en"><div class="title">Crazy <i>Title</i></div><p>Crazy Body</p><p>Really Crazy Body</p></div></div></body></html>"""

        result = load_body.scrap_body(data, 'pt')

        self.assertEqual(result, None)

    def test_scrapt_body_not_found(self):

        data = u"""<html><header></header><body><div class="content"></div></body></html>"""

        result = load_body.scrap_body(data, 'pt')

        self.assertEqual(result, None)

    def test_body_sample_1(self):
      data = ' '.join([i.strip() for i in codecs.open(os.path.dirname(__file__)+'/fixtures/body_sample_1.html', 'r', encoding='utf-8').readlines()])

      result = load_body.scrap_body(data, 'pt')

      # Text on the begining of the document
      self.assertTrue(u'On the one pot syntheses' in result)
      # Text on the end of the document
      self.assertTrue(u'Web Release Date: November 26, 2009' in result)

    def test_body_sample_2(self):
      data = ' '.join([i.strip() for i in codecs.open(os.path.dirname(__file__)+'/fixtures/body_sample_2.html', 'r', encoding='utf-8').readlines()])
      
      result = load_body.scrap_body(data, 'pt')

      # Text on the begining of the document
      self.assertTrue(u'meio para isolamento de' in result)
      # Text on the end of the document
      self.assertTrue(u'Recebido    para publicação em 31-7-1967' in result)

    def test_body_sample_3(self):
      data = ' '.join([i.strip() for i in codecs.open(os.path.dirname(__file__)+'/fixtures/body_sample_3.html', 'r', encoding='utf-8').readlines()])
      
      result = load_body.scrap_body(data, 'pt')

      # Text on the begining of the document
      self.assertTrue(u'A TRIBUTAÇÃO NA PRODUÇÃO DE CARVÃO VEGETAL' in result)
      # Text on the end of the document
      self.assertTrue(u'Recebido: 03 de Fevereiro de 2012; Aceito: 14 de Abril de 2014' in result)

    def test_body_sample_4(self):
      data = ' '.join([i.strip() for i in codecs.open(os.path.dirname(__file__)+'/fixtures/body_sample_4.html', 'r', encoding='utf-8').readlines()])
      
      result = load_body.scrap_body(data, 'pt')

      # Text on the begining of the document
      self.assertTrue(u'Aquarelas de um Brasil' in result)
      # Text on the end of the document
      self.assertTrue(u'São Paulo, Companhia das Letras.' in result)

    def test_body_sample_5(self):
      data = ' '.join([i.strip() for i in codecs.open(os.path.dirname(__file__)+'/fixtures/body_sample_5.html', 'r', encoding='utf-8').readlines()])
      
      result = load_body.scrap_body(data, 'pt')

      # Text on the begining of the document
      self.assertTrue(u'Molestia de Carlos Chagas' in result)
      # Text on the end of the document
      self.assertTrue(u'Full text available only in PDF format' in result)

    def test_body_sample_6(self):
      data = ' '.join([i.strip() for i in codecs.open(os.path.dirname(__file__)+'/fixtures/body_sample_6.html', 'r', encoding='utf-8').readlines()])
      
      result = load_body.scrap_body(data, 'pt')

      # Text on the begining of the document
      self.assertTrue(u'Editorial' in result)
      # Text on the end of the document
      self.assertTrue(u'Boa leitura!' in result)
