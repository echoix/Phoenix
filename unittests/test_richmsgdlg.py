import sys
import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class richmsgdlg_Tests(wtc.WidgetTestCase):

    # TODO: Maybe only one of the tests are hanging, not all of them
    @unittest.skipIf(sys.platform.startswith("win") and sys.version_info < (3, 10), "Hanging in windows CI")
    def test_richmsgdlg1(self):
        dlg = wx.RichMessageDialog(None, 'Message', 'Caption')
        wx.CallLater(250, dlg.EndModal, wx.ID_OK)
        dlg.ShowModal()
        dlg.Destroy()

    # TODO: Maybe only one of the tests are hanging, not all of them
    @unittest.skipIf(sys.platform.startswith("win") and sys.version_info < (3, 11), "Hanging in windows CI")
    def test_richmsgdlg2(self):
        dlg = wx.RichMessageDialog(self.frame, 'Message', 'Caption')
        wx.CallLater(250, dlg.EndModal, wx.ID_OK)
        dlg.ShowModal()
        dlg.Destroy()

    # TODO: Maybe only one of the tests are hanging, not all of them
    @unittest.skipIf(sys.platform.startswith("win") and sys.version_info < (3, 12), "Hanging in windows CI")
    def test_richmsgdlg3(self):
        dlg = wx.RichMessageDialog(None, 'Message', 'Caption')
        dlg.SetExtendedMessage('extended')
        dlg.SetMessage('message')
        dlg.SetOKCancelLabels('okidoky', 'bye-bye')
        self.assertEqual(dlg.GetExtendedMessage(), 'extended')
        self.assertEqual(dlg.GetMessage(), 'message')
        self.assertEqual(dlg.GetOKLabel(), 'okidoky')
        self.assertEqual(dlg.GetCancelLabel(), 'bye-bye')

        dlg.ShowCheckBox("Checkbox")
        dlg.ShowDetailedText("Detailed Text")
        self.assertEqual(dlg.GetCheckBoxText(), "Checkbox")
        self.assertEqual(dlg.GetDetailedText(), "Detailed Text")
        self.assertEqual(dlg.CheckBoxText, "Checkbox")
        self.assertEqual(dlg.DetailedText, "Detailed Text")

        wx.CallLater(250, dlg.EndModal, wx.ID_OK)
        dlg.ShowModal()
        dlg.Destroy()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
