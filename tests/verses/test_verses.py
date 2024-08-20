# from unittest import TestCase
# from src.words.splitter import WordSplitter
# from src.stress.finder import StressFinder
# from src.verses.splitter import VerseSplitter


# class TestVerseSpliter(TestCase):

#     def test_default(self):
#         splitter = WordSplitter()
#         finder   = StressFinder()
#         vsplitter = VerseSplitter(splitter, finder)

#         intext  = 'é ferida que dói, e não se sente;'
#         intext  = 'é ferida que dói,_e não se sente;'
#         # outtext = 'é|fe|ri|da|que|dói|e|não|se|sen|te'
#         # outtext = 'é|fe|ri|da|que|dói|e|não|se|sen|te'
#         result  = vsplitter.run(intext)
#         # self.assertEqual(result, outtext)

# #         intext  = 'é um contentamento descontente,'
# #         outtext = 'é|um|con|ten|ta|men|to|des|con|ten|te'
# #         result  = vsplitter.run(intext)
# #         self.assertEqual(result, outtext)

#         # intext  = 'é dor que desatina sem doer.'
#         # outtext = 'é|dor|que|de|sa|ti|na|sem|do|er'
#         # result  = vsplitter.run(intext)
#         # self.assertEqual(result, outtext)

#         # intext  = 'É um não querer mais que bem querer;'
#         # outtext = 'é|um|não|que|rer|mais|que|bem|que|rer'
#         # result  = vsplitter.run(intext)
#         # self.assertEqual(result, outtext)

# #         # intext  = 'É nunca contentar-se de contente;'
# #         # outtext = 'é|nun|ca|con|ten|tar|-se|de|con|ten|te'
# #         # result  = vsplitter(splitter, finder).run(intext)
# #         # self.assertEqual(result, outtext)

# #         # intext  = 'É um cuidar que ganha em se perder;'
# #         # outtext = 'é|um|cui|dar|que|ga|nha_em|se|per|der'
# #         # result  = vsplitter(splitter, finder).run(intext)
# #         # self.assertEqual(result, outtext)

# #         intext = 'Eu, filho do carbono e do amoníaco,'
# #         outtext = 'eu|fi|lho|do|car|bo|no_e|do_a|mo|ní|aco'
# #         result  = vsplitter.run(intext)
# #         self.assertEqual(result, outtext)

# #         intext = 'Monstro de escuridão e rutilância,'
# #         outtext = 'mons|tro|de_es|cu|ri|dão|e|ru|ti|lân|cia'
# #         result  = vsplitter.run(intext)
# #         self.assertEqual(result, outtext)



# #     def test_merge_hiatus(self):
# #         wsplitter = WordSplitter()
# #         finder    = StressFinder()
# #         vsplitter = VerseSplitter(wsplitter, finder, merge_hiatus=True)

# #         intext  = 'Amor é fogo que arde sem se ver,'
# #         outtext = 'a|mo|r_é|fo|go|que_ar|de|sem|se|ver'
# #         result  = vsplitter.run(intext)
# #         self.assertEqual(result, outtext)

# #         intext = 'A influência má dos signos do zodíaco.'
# #         outtext = 'a_in|flu_ên|ci_a|má|dos|si|gnos|do|zo|dí|aco'
# #         result  = vsplitter.run(intext)
# #         self.assertEqual(result, outtext)




# #     def test_3(self):
# #         wsplitter = WordSplitter()
# #         finder    = StressFinder()
# #         vsplitter = VerseSplitter(wsplitter, finder)
