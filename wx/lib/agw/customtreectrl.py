# --------------------------------------------------------------------------------- #
# CUSTOMTREECTRL wxPython IMPLEMENTATION
# Inspired By And Heavily Based On wxGenericTreeCtrl.
#
# Andrea Gavana, @ 17 May 2006
# Latest Revision: 02 Jul 2018, 00.10 GMT
# Modified by Helio Guilherme, @ 26 Apr 2018
#
# TODO List
#
# Almost All The Features Of wx.TreeCtrl Are Available, And There Is Practically
# No Limit In What Could Be Added To This Class. The First Things That Comes
# To My Mind Are:
#
# 1. Try To Implement A More Flicker-Free Background Image In Cases Like
#    Centered Or Stretched Image (Now CustomTreeCtrl Supports Only Tiled
#    Background Images).
#
# 2. Try To Mimic Windows wx.TreeCtrl Expanding/Collapsing behaviour: CustomTreeCtrl
#    Suddenly Expands/Collapses The Nodes On Mouse Click While The Native Control
#    Has Some Kind Of "Smooth" Expanding/Collapsing, Like A Wave. I Don't Even
#    Know Where To Start To Do That.
#
# 3. Speed Up General OnPaint Things? I Have No Idea, Here CustomTreeCtrl Is Quite
#    Fast, But We Should See On Slower Machines.
#
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To Me At:
#
# andrea.gavana@maerskoil.com
# andrea.gavana@gmail.com
#
# Or, Obviously, To The wxPython Mailing List!!!
#
# Tags:        phoenix-port, unittest, documented, py3-port
#
# End Of Comments
# --------------------------------------------------------------------------------- #


"""
The ``customtreectrl`` module contains the :class:`~wx.lib.agw.customtreectrl.CustomTreeCtrl` class
which mimics the behaviour of :class:`TreeCtrl`, with some more enhancements.


Description
===========

:class:`CustomTreeCtrl` is a class that mimics the behaviour of :class:`TreeCtrl`, with almost the
same base functionalities plus some more enhancements. This class does not rely on
the native control, as it is a full owner-drawn tree control.
Apart of the base functionalities of :class:`CustomTreeCtrl` (described below), in addition
to the standard :class:`TreeCtrl` behaviour this class supports:

* CheckBox-type items: checkboxes are easy to handle, just selected or unselected
  state with no particular issues in handling the item's children;
* Added support for 3-state value checkbox items;
* RadioButton-type items: since I elected to put radiobuttons in :class:`CustomTreeCtrl`, I
  needed some way to handle them, that made sense. So, I used the following approach:

  - All peer-nodes that are radiobuttons will be mutually exclusive. In other words,
    only one of a set of radiobuttons that share a common parent can be checked at
    once. If a radiobutton node becomes checked, then all of its peer radiobuttons
    must be unchecked.
  - If a radiobutton node becomes unchecked, then all of its child nodes will become
    inactive.

* Hyperlink-type items: they look like an hyperlink, with the proper mouse cursor on
  hovering;
* Multiline text items (**note**: to add a newline character in a multiline item, press
  ``Shift`` + ``Enter`` as the ``Enter`` key alone is consumed by :class:`CustomTreeCtrl` to finish
  the editing and ``Ctrl`` + ``Enter`` is consumed by the platform for tab navigation);
* Enabling/disabling items (together with their plain or grayed out icons);
* Whatever non-toplevel widget can be attached next to an item;
* Possibility to horizontally align the widgets attached to tree items on the
  same tree level.
* Possibility to align the widgets attached to tree items to the rightmost edge of :class:`CustomTreeCtrl`;
* Default selection style, gradient (horizontal/vertical) selection style and Windows
  Vista selection style;
* Customized drag and drop images built on the fly;
* Setting the :class:`CustomTreeCtrl` item buttons to a personalized imagelist;
* Setting the :class:`CustomTreeCtrl` check/radio item icons to a personalized imagelist;
* Changing the style of the lines that connect the items (in terms of :class:`wx.Pen` styles);
* Using an image as a :class:`CustomTreeCtrl` background (currently only in "tile" mode);
* Adding images to any item in the leftmost area of the :class:`CustomTreeCtrl` client window.
* Separator-type items which are simply visual indicators that are meant to set apart
  or divide tree items, with the following caveats:

  - Separator items should not have children, labels, data or an associated window;
  - You can change the color of individual separators by using :meth:`~CustomTreeCtrl.SetItemTextColour`, or you can use
    :meth:`~CustomTreeCtrl.SetSeparatorColour` to change the color of all separators. The default separator colour
    is that returned by `SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)`;
  - Separators can be selected just like any other tree item;
  - Separators cannot have text;
  - Separators cannot have children;
  - Separators cannot be edited via the ``EVT_TREE_BEGIN_LABEL_EDIT`` event.

* Ellipsization of long items when the horizontal space is low, via the ``TR_ELLIPSIZE_LONG_ITEMS``
  style (`New in version 0.9.3`);
* Tooltips on long items when the horizontal space is low, via the ``TR_TOOLTIP_ON_LONG_ITEMS``
  style (`New in version 0.9.3`).
* Hiding items

And a lot more. Check the demo for an almost complete review of the functionalities.


Base Functionalities
====================

:class:`CustomTreeCtrl` supports all the :class:`TreeCtrl` styles, except:

- ``TR_EXTENDED``: supports for this style is on the todo list (am I sure of this?).

Plus it has 3 more styles to handle checkbox-type items:

- ``TR_AUTO_CHECK_CHILD``: automatically checks/unchecks the item children;
- ``TR_AUTO_CHECK_PARENT``: automatically checks/unchecks the item parent;
- ``TR_AUTO_TOGGLE_CHILD``: automatically toggles the item children.

And two styles you can use to force the horizontal alignment of all the widgets
attached to the tree items:

- ``TR_ALIGN_WINDOWS``: aligns horizontally the windows belonging to the item on the
  same tree level.
- ``TR_ALIGN_WINDOWS_RIGHT``: aligns to the rightmost position the windows belonging
  to the item on the same tree level.

And two styles related to long items (with a lot of text in them), which can be
ellipsized and/or highlighted with a tooltip:

- ``TR_ELLIPSIZE_LONG_ITEMS``: ellipsizes long items when the horizontal space for
  :class:`CustomTreeCtrl` is low (`New in version 0.9.3`);
- ``TR_TOOLTIP_ON_LONG_ITEMS``: shows tooltips on long items when the horizontal space
  for :class:`CustomTreeCtrl` is low (`New in version 0.9.3`);.

All the methods available in :class:`TreeCtrl` are also available in :class:`CustomTreeCtrl`.


Usage
=====

Usage example::

    import wx
    import wx.lib.agw.customtreectrl as CT

    class MyFrame(wx.Frame):

        def __init__(self, parent):

            wx.Frame.__init__(self, parent, -1, "CustomTreeCtrl Demo")

            # Create a CustomTreeCtrl instance
            custom_tree = CT.CustomTreeCtrl(self, agwStyle=wx.TR_DEFAULT_STYLE)

            # Add a root node to it
            root = custom_tree.AddRoot("The Root Item")

            # Create an image list to add icons next to an item
            il = wx.ImageList(16, 16)
            fldridx     = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, (16, 16)))
            fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, (16, 16)))
            fileidx     = il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16)))

            custom_tree.SetImageList(il)

            custom_tree.SetItemImage(root, fldridx, wx.TreeItemIcon_Normal)
            custom_tree.SetItemImage(root, fldropenidx, wx.TreeItemIcon_Expanded)

            for x in range(15):
                child = custom_tree.AppendItem(root, "Item %d" % x)
                custom_tree.SetItemImage(child, fldridx, wx.TreeItemIcon_Normal)
                custom_tree.SetItemImage(child, fldropenidx, wx.TreeItemIcon_Expanded)

                for y in range(5):
                    last = custom_tree.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)))
                    custom_tree.SetItemImage(last, fldridx, wx.TreeItemIcon_Normal)
                    custom_tree.SetItemImage(last, fldropenidx, wx.TreeItemIcon_Expanded)

                    for z in range(5):
                        item = custom_tree.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z))
                        custom_tree.SetItemImage(item, fileidx, wx.TreeItemIcon_Normal)

            custom_tree.Expand(root)


    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()



Events
======

All the events supported by :class:`TreeCtrl` are also available in :class:`CustomTreeCtrl`, with
a few exceptions:

- ``EVT_TREE_GET_INFO`` (don't know what this means);
- ``EVT_TREE_SET_INFO`` (don't know what this means);
- ``EVT_TREE_ITEM_MIDDLE_CLICK`` (not implemented, but easy to add);
- ``EVT_TREE_STATE_IMAGE_CLICK`` (no need for that, look at the checking events below).

Plus, :class:`CustomTreeCtrl` supports the events related to the checkbutton-type items:

- ``EVT_TREE_ITEM_CHECKING``: an item is being checked;
- ``EVT_TREE_ITEM_CHECKED``: an item has been checked.

And to hyperlink-type items:

- ``EVT_TREE_ITEM_HYPERLINK``: an hyperlink item has been clicked (this event is sent
  after the ``EVT_TREE_SEL_CHANGED`` event).


Drag and Drop
=============

A simplified drag and drop is available and can be initiated by calling
``event.Allow`` on the ``EVT_TREE_BEGIN_DRAG`` or ``EVT_TREE_BEGIN_RDRAG``
events. When the event handler returns, a ``wx.DragImage`` of the item will be
generated and the user can drag it to other items within the tree. When the
user releases the drag button a ``EVT_TREE_END_DRAG`` event will be sent and
``event.GetItem`` can be called to find out which item the drag ended at.
This simplified method is best when only a single item at a time needs to
be dragged (i.e. ``TR_MULTIPLE`` not set) and only for dragging items within
the tree control.

Alternately, the normal wxPython drag/drop can be invoked in the ``EVT_TREE_BEGIN_DRAG``
handler in which a :class:`wx.DropSource` must be generated, followed by a call
to :meth:`~wx.DropSource.DoDragDrop` which will block until the drag is finished.
This is much more flexible but more complicated to implement.

:note: The class value _DRAG_TIMER_TICKS controls how long the mouse must
 linger before the drag can start. It defaults to 250 milliseconds which can
 be far too long for today's quick 'swiping' generation. It can be lowered for
 a more responsive drag.


Supported Platforms
===================

:class:`CustomTreeCtrl` has been tested on the following platforms:
  * Windows (Windows XP);
  * GTK (Thanks to Michele Petrazzo);
  * Mac OS (Thanks to John Jackson).


Window Styles
=============

This class takes in a regular wxPython ``style`` and an extended ``agwStyle``.
The ``style`` can be used with normal wxPython styles such as ``wx.WANTS_CHARS``
while the ``agwStyle`` specifies the behavior of the tree itself.
It supports the following ``agwStyle`` flags:

================================= =========== ==================================================
Window agwStyle Flags             Hex Value   Description
================================= =========== ==================================================
**wx.TR_DEFAULT_STYLE**              *varies* The set of flags that are closest to the defaults for the native control for a particular toolkit.  Should always be used.
``wx.TR_NO_BUTTONS``                      0x0 For convenience to document that no buttons are to be drawn.
``wx.TR_SINGLE``                          0x0 For convenience to document that only one item may be selected at a time. Selecting another item causes the current selection, if any, to be deselected. This is the default.
``wx.TR_HAS_BUTTONS``                     0x1 Use this style to show + and - buttons to the left of parent items.
``wx.TR_NO_LINES``                        0x4 Use this style to hide vertical level connectors.
``wx.TR_LINES_AT_ROOT``                   0x8 Use this style to show lines between root nodes. Only applicable if ``TR_HIDE_ROOT`` is set and ``TR_NO_LINES`` is not set.
``wx.TR_TWIST_BUTTONS``                  0x10 Use old Mac-twist style buttons.
``wx.TR_MULTIPLE``                       0x20 Use this style to allow a range of items to be selected. If a second range is selected, the current range, if any, is deselected.
``wx.TR_HAS_VARIABLE_ROW_HEIGHT``        0x80 Use this style to cause row heights to be just big enough to fit the content. If not set, all rows use the largest row height. The default is that this flag is unset.
``wx.TR_EDIT_LABELS``                   0x200 Use this style if you wish the user to be able to edit labels in the tree control.
``wx.TR_ROW_LINES``                     0x400 Use this style to draw a contrasting border between displayed rows.
``wx.TR_HIDE_ROOT``                     0x800 Use this style to suppress the display of the root node, effectively causing the first-level nodes to appear as a series of root nodes.
``wx.TR_FULL_ROW_HIGHLIGHT``           0x2000 Use this style to have the background colour and the selection highlight extend  over the entire horizontal row of the tree control window.
**Styles from customtreectrl:**
``TR_EXTENDED``                          0x40 Use this style to allow disjoint items to be selected. (Only partially implemented; may not work in all cases).
``TR_AUTO_CHECK_CHILD``                0x4000 Only meaningful for checkbox-type items: when a parent item is checked/unchecked its children are checked/unchecked as well.
``TR_AUTO_TOGGLE_CHILD``               0x8000 Only meaningful for checkbox-type items: when a parent item is checked/unchecked its children are toggled accordingly.
``TR_AUTO_CHECK_PARENT``              0x10000 Only meaningful for checkbox-type items: when a child item is checked/unchecked its parent item is checked/unchecked as well.
``TR_ALIGN_WINDOWS``                  0x20000 Flag used to align windows (in items with windows) at the same horizontal position.
``TR_ALIGN_WINDOWS_RIGHT``            0x40000 Flag used to align windows (in items with windows) to the rightmost edge of :class:`CustomTreeCtrl`.
``TR_ELLIPSIZE_LONG_ITEMS``           0x80000 Flag used to ellipsize long items when the horizontal space for :class:`CustomTreeCtrl` is low.
``TR_TOOLTIP_ON_LONG_ITEMS``         0x100000 Flag used to show tooltips on long items when the horizontal space for :class:`CustomTreeCtrl` is low.
================================= =========== ==================================================

The ``wx.TR_HAS_VARIABLE_LINE_HEIGHT`` style should be set if item rows might
not all be the same height. This can happen if certain rows have a larger font
size, multi-line text, or windows added to them. This style will automatically
adjust each item's height to be just big enough to show its contents.

When the ``wx.TR_HAS_VARIABLE_LINE_HEIGHT`` is not set, adding a new item with
multi-line text or with a window specified will throw an exception. However the
tree won't prevent you from adding multiline text with :meth:`~TreeListMainWindow.SetItemText`
or assigning a window with :meth:`~TreeListMainWindow.SetItemWindow` to an
existing item. It's generally a bad idea to do either of these without this
style as it will result in an ugly tree. By default the ``wx.TR_HAS_VARIABLE_LINE_HEIGHT``
is not set. This means that all item rows will use the same height. This is the
height of the largest item in the tree. If an item with a larger height is
added or revealed, ALL row heights will increase to this larger size. The
larger row height remains persistent even if the large items are hidden or
deleted. You must call :meth:`~wx.lib.agw.customtreectrl.CustomTreeCtrl.CalculateLineHeight`
to reset the row height. This somewhat bizarre behavior is why the ``wx.TR_HAS_VARIABLE_LINE_HEIGHT``
style is almost always used.


Events Processing
=================

This class processes the following events:

============================== ==================================================
Event Name                     Description
============================== ==================================================
``EVT_TREE_BEGIN_DRAG``        Begin dragging with the left mouse button.
``EVT_TREE_BEGIN_LABEL_EDIT``  Begin editing a label. This can be prevented by calling :meth:`~TreeEvent.Veto`.
``EVT_TREE_BEGIN_RDRAG``       Begin dragging with the right mouse button.
``EVT_TREE_DELETE_ITEM``       Delete an item.
``EVT_TREE_END_DRAG``          End dragging with the left or right mouse button.
``EVT_TREE_END_LABEL_EDIT``    End editing a label. This can be prevented by calling :meth:`~TreeEvent.Veto`.
``EVT_TREE_GET_INFO``          Request information from the application (not implemented in :class:`CustomTreeCtrl`).
``EVT_TREE_ITEM_ACTIVATED``    The item has been activated, i.e. chosen by double clicking it with mouse or from keyboard.
``EVT_TREE_ITEM_CHECKED``      A checkbox or radiobox type item has been checked.
``EVT_TREE_ITEM_CHECKING``     A checkbox or radiobox type item is being checked.
``EVT_TREE_ITEM_COLLAPSED``    The item has been collapsed.
``EVT_TREE_ITEM_COLLAPSING``   The item is being collapsed. This can be prevented by calling :meth:`~TreeEvent.Veto`.
``EVT_TREE_ITEM_EXPANDED``     The item has been expanded.
``EVT_TREE_ITEM_EXPANDING``    The item is being expanded. This can be prevented by calling :meth:`~TreeEvent.Veto`.
``EVT_TREE_ITEM_GETTOOLTIP``   The opportunity to set the item tooltip is being given to the application (call `TreeEvent.SetToolTip`).
``EVT_TREE_ITEM_HYPERLINK``    An hyperlink type item has been clicked.
``EVT_TREE_ITEM_MENU``         The context menu for the selected item has been requested, either by a right click or by using the menu key.
``EVT_TREE_ITEM_MIDDLE_CLICK`` The user has clicked the item with the middle mouse button (not implemented in :class:`CustomTreeCtrl`).
``EVT_TREE_ITEM_RIGHT_CLICK``  The user has clicked the item with the right mouse button.
``EVT_TREE_KEY_DOWN``          A key has been pressed.
``EVT_TREE_SEL_CHANGED``       Selection has changed.
``EVT_TREE_SEL_CHANGING``      Selection is changing. This can be prevented by calling :meth:`~TreeEvent.Veto`.
``EVT_TREE_SET_INFO``          Information is being supplied to the application (not implemented in :class:`CustomTreeCtrl`).
``EVT_TREE_STATE_IMAGE_CLICK`` The state image has been clicked (not implemented in :class:`CustomTreeCtrl`).
============================== ==================================================


License And Version
===================

:class:`CustomTreeCtrl` is distributed under the wxPython license.

Latest Revision: Helio Guilherme @ 09 Aug 2018, 21.35 GMT

Version 2.7

"""

# Version Info
__version__ = "2.7"

import wx
from wx.lib.expando import ExpandoTextCtrl

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

_NO_IMAGE = -1
_PIXELS_PER_UNIT = 10

# Start editing the current item after half a second (if the mouse hasn't
# been clicked/moved)
_DELAY = 500

# wxPython version string
_VERSION_STRING = wx.VERSION_STRING

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

# Enum for different images associated with a treectrl item
TreeItemIcon_Normal = 0              # not selected, not expanded
""" The tree item is not selected and not expanded. """
TreeItemIcon_Selected = 1            #     selected, not expanded
""" The tree item is selected and not expanded. """
TreeItemIcon_Expanded = 2            # not selected,     expanded
""" The tree item is not selected but expanded. """
TreeItemIcon_SelectedExpanded = 3    #     selected,     expanded
""" The tree item is selected and expanded. """
TreeItemIcon_Checked = 0             # check button,     checked
""" The item's check button is checked. """
TreeItemIcon_NotChecked = 1          # check button, not checked
""" The item's check button is not checked. """
TreeItemIcon_Undetermined = 2        # check button, undetermined
""" The item's check button is in undetermined state (used only for a 3-state check button). """
TreeItemIcon_Flagged = 3             # radio button,     selected
""" The item's radio button is checked. """
TreeItemIcon_NotFlagged = 4          # radio button, not selected
""" The item's radio button is not checked. """

# ----------------------------------------------------------------------------
# CustomTreeCtrl flags
# ----------------------------------------------------------------------------

TR_NO_BUTTONS = wx.TR_NO_BUTTONS                               # for convenience
""" For convenience to document that no buttons are to be drawn. """
TR_HAS_BUTTONS = wx.TR_HAS_BUTTONS                             # draw collapsed/expanded btns
""" Use this style to show + and - buttons to the left of parent items. """
TR_NO_LINES = wx.TR_NO_LINES                                   # don't draw lines at all
""" Use this style to hide vertical level connectors. """
TR_LINES_AT_ROOT = wx.TR_LINES_AT_ROOT                         # connect top-level nodes
""" Use this style to show lines between root nodes. Only applicable if ``TR_HIDE_ROOT`` is set and ``TR_NO_LINES`` is not set. """
TR_TWIST_BUTTONS = wx.TR_TWIST_BUTTONS                         # still used by wxTreeListCtrl
""" Use old Mac-twist style buttons. """
TR_SINGLE = wx.TR_SINGLE                                       # for convenience
""" For convenience to document that only one item may be selected at a time. Selecting another item causes the current selection, if any, to be deselected. This is the default. """
TR_MULTIPLE = wx.TR_MULTIPLE                                   # can select multiple items
""" Use this style to allow a range of items to be selected. If a second range is selected, the current range, if any, is deselected. """
TR_EXTENDED = 0x40                                             # TODO: allow extended selection
""" Use this style to allow disjoint items to be selected. (Only partially implemented; may not work in all cases). """
TR_HAS_VARIABLE_ROW_HEIGHT = wx.TR_HAS_VARIABLE_ROW_HEIGHT     # what it says
""" Use this style to cause row heights to be just big enough to fit the content. If not set, all rows use the largest row height. The default is that this flag is unset. """
TR_EDIT_LABELS = wx.TR_EDIT_LABELS                             # can edit item labels
""" Use this style if you wish the user to be able to edit labels in the tree control. """
TR_ROW_LINES = wx.TR_ROW_LINES                                 # put border around items
""" Use this style to draw a contrasting border between displayed rows. """
TR_HIDE_ROOT = wx.TR_HIDE_ROOT                                 # don't display root node
""" Use this style to suppress the display of the root node, effectively causing the first-level nodes to appear as a series of root nodes. """
TR_FULL_ROW_HIGHLIGHT = wx.TR_FULL_ROW_HIGHLIGHT               # highlight full horz space
""" Use this style to have the background colour and the selection highlight extend over the entire horizontal row of the tree control window. """

TR_AUTO_CHECK_CHILD = 0x04000                                  # only meaningful for checkboxes
""" Only meaningful for checkbox-type items: when a parent item is checked/unchecked its children are checked/unchecked as well. """
TR_AUTO_TOGGLE_CHILD = 0x08000                                 # only meaningful for checkboxes
""" Only meaningful for checkbox-type items: when a parent item is checked/unchecked its children are toggled accordingly. """
TR_AUTO_CHECK_PARENT = 0x10000                                 # only meaningful for checkboxes
""" Only meaningful for checkbox-type items: when a child item is checked/unchecked its parent item is checked/unchecked as well. """
TR_ALIGN_WINDOWS = 0x20000                                     # to align windows horizontally for items at the same level
""" Flag used to align windows (in items with windows) at the same horizontal position. """
TR_ALIGN_WINDOWS_RIGHT = 0x40000                               # to align windows to the rightmost edge of CustomTreeCtrl
""" Flag used to align windows (in items with windows) to the rightmost edge of :class:`CustomTreeCtrl`."""
TR_ELLIPSIZE_LONG_ITEMS = 0x80000                              # to ellipsize long items when horizontal space is low
""" Flag used to ellipsize long items when the horizontal space for :class:`CustomTreeCtrl` is low."""
TR_TOOLTIP_ON_LONG_ITEMS = 0x100000                            # to display tooltips on long items when horizontal space is low
""" Flag used to show tooltips on long items when the horizontal space for :class:`CustomTreeCtrl` is low."""

TR_DEFAULT_STYLE = wx.TR_DEFAULT_STYLE                         # default style for the tree control
""" The set of flags that are closest to the defaults for the native control for a particular toolkit. """

# Values for the `flags` parameter of CustomTreeCtrl.HitTest() which determine
# where exactly the specified point is situated:

TREE_HITTEST_ABOVE            = wx.TREE_HITTEST_ABOVE
""" Above the client area. """
TREE_HITTEST_BELOW            = wx.TREE_HITTEST_BELOW
""" Below the client area. """
TREE_HITTEST_NOWHERE          = wx.TREE_HITTEST_NOWHERE
""" No item has been hit. """
TREE_HITTEST_ONITEMBUTTON     = wx.TREE_HITTEST_ONITEMBUTTON
""" On the button associated with an item. """
TREE_HITTEST_ONITEMICON       = wx.TREE_HITTEST_ONITEMICON
""" On the bitmap associated with an item. """
TREE_HITTEST_ONITEMINDENT     = wx.TREE_HITTEST_ONITEMINDENT
""" On the indent associated with an item. """
TREE_HITTEST_ONITEMLABEL      = wx.TREE_HITTEST_ONITEMLABEL
""" On the label (string) associated with an item. """
TREE_HITTEST_ONITEMRIGHT      = wx.TREE_HITTEST_ONITEMRIGHT
""" On the right of the label associated with an item. """
TREE_HITTEST_ONITEMSTATEICON  = wx.TREE_HITTEST_ONITEMSTATEICON
""" On the right of the label associated with an item. """
TREE_HITTEST_TOLEFT           = wx.TREE_HITTEST_TOLEFT
""" On the left of an item. """
TREE_HITTEST_TORIGHT          = wx.TREE_HITTEST_TORIGHT
""" On the right of an item. """
TREE_HITTEST_ONITEMUPPERPART  = wx.TREE_HITTEST_ONITEMUPPERPART
""" On the upper part (first half) of the item. """
TREE_HITTEST_ONITEMLOWERPART  = wx.TREE_HITTEST_ONITEMLOWERPART
""" On the lower part (second half) of the item. """
TREE_HITTEST_ONITEMCHECKICON  = 0x4000
""" On the check icon, if present. """
TREE_HITTEST_ONITEM  = TREE_HITTEST_ONITEMICON | TREE_HITTEST_ONITEMLABEL | TREE_HITTEST_ONITEMCHECKICON
""" Anywhere on the item. """

TREE_ITEMTYPE_NORMAL = 0
""" A normal item. """
TREE_ITEMTYPE_CHECK = 1
""" A checkbox-like item. """
TREE_ITEMTYPE_RADIO = 2
""" A radiobutton-like item. """

# Background Image Style
_StyleTile = 0
_StyleStretch = 1

# Windows Vista Colours
_rgbSelectOuter = wx.Colour(170, 200, 245)
_rgbSelectInner = wx.Colour(230, 250, 250)
_rgbSelectTop = wx.Colour(210, 240, 250)
_rgbSelectBottom = wx.Colour(185, 215, 250)
_rgbNoFocusTop = wx.Colour(250, 250, 250)
_rgbNoFocusBottom = wx.Colour(235, 235, 235)
_rgbNoFocusOuter = wx.Colour(220, 220, 220)
_rgbNoFocusInner = wx.Colour(245, 245, 245)

# Flags for wx.RendererNative
_CONTROL_EXPANDED = 8
_CONTROL_CURRENT = 16


# ----------------------------------------------------------------------------
# CustomTreeCtrl events and binding for handling them
# ----------------------------------------------------------------------------

wxEVT_TREE_BEGIN_DRAG = wx.wxEVT_COMMAND_TREE_BEGIN_DRAG
wxEVT_TREE_BEGIN_RDRAG = wx.wxEVT_COMMAND_TREE_BEGIN_RDRAG
wxEVT_TREE_BEGIN_LABEL_EDIT = wx.wxEVT_COMMAND_TREE_BEGIN_LABEL_EDIT
wxEVT_TREE_END_LABEL_EDIT = wx.wxEVT_COMMAND_TREE_END_LABEL_EDIT
wxEVT_TREE_DELETE_ITEM = wx.wxEVT_COMMAND_TREE_DELETE_ITEM
wxEVT_TREE_GET_INFO = wx.wxEVT_COMMAND_TREE_GET_INFO
wxEVT_TREE_SET_INFO = wx.wxEVT_COMMAND_TREE_SET_INFO
wxEVT_TREE_ITEM_EXPANDED = wx.wxEVT_COMMAND_TREE_ITEM_EXPANDED
wxEVT_TREE_ITEM_EXPANDING = wx.wxEVT_COMMAND_TREE_ITEM_EXPANDING
wxEVT_TREE_ITEM_COLLAPSED = wx.wxEVT_COMMAND_TREE_ITEM_COLLAPSED
wxEVT_TREE_ITEM_COLLAPSING = wx.wxEVT_COMMAND_TREE_ITEM_COLLAPSING
wxEVT_TREE_SEL_CHANGED = wx.wxEVT_COMMAND_TREE_SEL_CHANGED
wxEVT_TREE_SEL_CHANGING = wx.wxEVT_COMMAND_TREE_SEL_CHANGING
wxEVT_TREE_KEY_DOWN = wx.wxEVT_COMMAND_TREE_KEY_DOWN
wxEVT_TREE_ITEM_ACTIVATED = wx.wxEVT_COMMAND_TREE_ITEM_ACTIVATED
wxEVT_TREE_ITEM_RIGHT_CLICK = wx.wxEVT_COMMAND_TREE_ITEM_RIGHT_CLICK
wxEVT_TREE_ITEM_MIDDLE_CLICK = wx.wxEVT_COMMAND_TREE_ITEM_MIDDLE_CLICK
wxEVT_TREE_END_DRAG = wx.wxEVT_COMMAND_TREE_END_DRAG
wxEVT_TREE_STATE_IMAGE_CLICK = wx.wxEVT_COMMAND_TREE_STATE_IMAGE_CLICK
wxEVT_TREE_ITEM_GETTOOLTIP = wx.wxEVT_COMMAND_TREE_ITEM_GETTOOLTIP
wxEVT_TREE_ITEM_MENU = wx.wxEVT_COMMAND_TREE_ITEM_MENU
wxEVT_TREE_ITEM_CHECKING = wx.NewEventType()
wxEVT_TREE_ITEM_CHECKED = wx.NewEventType()
wxEVT_TREE_ITEM_HYPERLINK = wx.NewEventType()

EVT_TREE_BEGIN_DRAG = wx.EVT_TREE_BEGIN_DRAG
""" Begin dragging with the left mouse button. """
EVT_TREE_BEGIN_RDRAG = wx.EVT_TREE_BEGIN_RDRAG
""" Begin dragging with the right mouse button. """
EVT_TREE_BEGIN_LABEL_EDIT = wx.EVT_TREE_BEGIN_LABEL_EDIT
""" Begin editing a label. This can be prevented by calling :meth:`~TreeEvent.Veto`. """
EVT_TREE_END_LABEL_EDIT = wx.EVT_TREE_END_LABEL_EDIT
""" End editing a label. This can be prevented by calling :meth:`~TreeEvent.Veto`. """
EVT_TREE_DELETE_ITEM = wx.EVT_TREE_DELETE_ITEM
""" Delete an item. """
EVT_TREE_GET_INFO = wx.EVT_TREE_GET_INFO
""" Request information from the application (not implemented in :class:`CustomTreeCtrl`). """
EVT_TREE_SET_INFO = wx.EVT_TREE_SET_INFO
""" Information is being supplied to the application (not implemented in :class:`CustomTreeCtrl`). """
EVT_TREE_ITEM_EXPANDED = wx.EVT_TREE_ITEM_EXPANDED
""" The item has been expanded. """
EVT_TREE_ITEM_EXPANDING = wx.EVT_TREE_ITEM_EXPANDING
""" The item is being expanded. This can be prevented by calling :meth:`~TreeEvent.Veto`. """
EVT_TREE_ITEM_COLLAPSED = wx.EVT_TREE_ITEM_COLLAPSED
""" The item has been collapsed. """
EVT_TREE_ITEM_COLLAPSING = wx.EVT_TREE_ITEM_COLLAPSING
""" The item is being collapsed. This can be prevented by calling :meth:`~TreeEvent.Veto`. """
EVT_TREE_SEL_CHANGED = wx.EVT_TREE_SEL_CHANGED
""" Selection has changed. """
EVT_TREE_SEL_CHANGING = wx.EVT_TREE_SEL_CHANGING
""" Selection is changing. This can be prevented by calling :meth:`~TreeEvent.Veto`. """
EVT_TREE_KEY_DOWN = wx.EVT_TREE_KEY_DOWN
""" A key has been pressed. """
EVT_TREE_ITEM_ACTIVATED = wx.EVT_TREE_ITEM_ACTIVATED
""" The item has been activated, i.e. chosen by double clicking it with mouse or from keyboard. """
EVT_TREE_ITEM_RIGHT_CLICK = wx.EVT_TREE_ITEM_RIGHT_CLICK
""" The user has clicked the item with the right mouse button. """
EVT_TREE_ITEM_MIDDLE_CLICK = wx.EVT_TREE_ITEM_MIDDLE_CLICK
""" The user has clicked the item with the middle mouse button (not implemented in :class:`CustomTreeCtrl`). """
EVT_TREE_END_DRAG = wx.EVT_TREE_END_DRAG
""" End dragging with the left or right mouse button. """
EVT_TREE_STATE_IMAGE_CLICK = wx.EVT_TREE_STATE_IMAGE_CLICK
""" The state image has been clicked (not implemented in :class:`CustomTreeCtrl`). """
EVT_TREE_ITEM_GETTOOLTIP = wx.EVT_TREE_ITEM_GETTOOLTIP
""" The opportunity to set the item tooltip is being given to the application (call `TreeEvent.SetToolTip`). """
EVT_TREE_ITEM_MENU = wx.EVT_TREE_ITEM_MENU
""" The context menu for the selected item has been requested, either by a right click or by using the menu key. """
EVT_TREE_ITEM_CHECKING = wx.PyEventBinder(wxEVT_TREE_ITEM_CHECKING, 1)
""" A checkbox or radiobox type item is being checked. """
EVT_TREE_ITEM_CHECKED = wx.PyEventBinder(wxEVT_TREE_ITEM_CHECKED, 1)
""" A checkbox or radiobox type item has been checked. """
EVT_TREE_ITEM_HYPERLINK = wx.PyEventBinder(wxEVT_TREE_ITEM_HYPERLINK, 1)
""" An hyperlink type item has been clicked. """


# ----------------------------------------------------------------------------

def MakeDisabledBitmap(original):
    """
    Creates a disabled-looking bitmap starting from the input one.

    :param `original`: an instance of :class:`wx.Bitmap` to be greyed-out.

    :return: An instance of :class:`wx.Bitmap`, containing a disabled-looking
     representation of the original item image.
    """

    img = original.ConvertToImage()
    return wx.Bitmap(img.ConvertToGreyscale())

# ----------------------------------------------------------------------------

def DrawTreeItemButton(win, dc, rect, flags):
    """
    Draw the expanded/collapsed icon for a tree control item.

    :param `win`: an instance of :class:`wx.Window`;
    :param `dc`: an instance of :class:`wx.DC`;
    :param wx.Rect `rect`: the client rectangle where to draw the tree item button;
    :param integer `flags`: contains ``wx.CONTROL_EXPANDED`` bit for expanded tree items.

    :note: This is a simple replacement of :meth:`RendererNative.DrawTreeItemButton`.

    :note: This method is never used in wxPython versions newer than 2.6.2.1.
    """

    # white background
    dc.SetPen(wx.GREY_PEN)
    dc.SetBrush(wx.WHITE_BRUSH)
    dc.DrawRectangle(rect)

    # black lines
    xMiddle = rect.x + rect.width//2
    yMiddle = rect.y + rect.height//2

    # half of the length of the horz lines in "-" and "+"
    halfWidth = rect.width//2 - 2
    dc.SetPen(wx.BLACK_PEN)
    dc.DrawLine(xMiddle - halfWidth, yMiddle,
                xMiddle + halfWidth + 1, yMiddle)

    if not flags & _CONTROL_EXPANDED:

        # turn "-" into "+"
        halfHeight = rect.height//2 - 2
        dc.DrawLine(xMiddle, yMiddle - halfHeight,
                    xMiddle, yMiddle + halfHeight + 1)

# ----------------------------------------------------------------------------

def EventFlagsToSelType(style, shiftDown=False, ctrlDown=False):
    """
    Translate the key or mouse event flag to the type of selection we
    are dealing with.

    :param integer `style`: the main :class:`CustomTreeCtrl` window style flag;
    :param bool `shiftDown`: ``True`` if the ``Shift`` key is pressed, ``False`` otherwise;
    :param bool `ctrlDown`: ``True`` if the ``Ctrl`` key is pressed, ``False`` otherwise;

    :return: A 3-elements tuple, with the following elements:

     - `is_multiple`: ``True`` if :class:`CustomTreeCtrl` has the ``TR_MULTIPLE`` flag set, ``False`` otherwise;
     - `extended_select`: ``True`` if the ``Shift`` key is pressend and if :class:`CustomTreeCtrl` has the
       ``TR_MULTIPLE`` flag set, ``False`` otherwise;
     - `unselect_others`: ``True`` if the ``Ctrl`` key is pressend and if :class:`CustomTreeCtrl` has the
       ``TR_MULTIPLE`` flag set, ``False`` otherwise.
    """

    is_multiple = (style & TR_MULTIPLE) != 0
    extended_select = shiftDown and is_multiple
    unselect_others = not (extended_select or (ctrlDown and is_multiple))

    return is_multiple, extended_select, unselect_others

# ----------------------------------------------------------------------------

def ChopText(dc, text, max_size):
    """
    Chops the input `text` if its size does not fit in `max_size`, by cutting the
    text and adding ellipsis at the end.

    :param `dc`: a :class:`wx.DC` device context;
    :param `text`: the text to chop;
    :param `max_size`: the maximum size in which the text should fit.

    :note: This method is used exclusively when :class:`CustomTreeCtrl` has the ``TR_ELLIPSIZE_LONG_ITEMS``
     style set.

    .. versionadded:: 0.9.3
    """

    # first check if the text fits with no problems (converts to Unicode).
    x, y, dummy = dc.GetFullMultiLineTextExtent(text)

    if x <= max_size:
        return text

    # We cannot chop text that is UTF-8, as it could produce invalid sequences.
    if isinstance(text, bytes):
        # Convert UTF-8 (Phoenix's mandatory encoding) to Unicode.
        text = text.decode('utf-8')
    textLen = len(text)
    last_good_length = 0

    for i in range(textLen, -1, -1):
        s = text[0:i]
        s += "..."

        x, y = dc.GetTextExtent(s)
        last_good_length = i

        if x < max_size:
            break

    ret = text[0:last_good_length] + "..."
    return ret


#---------------------------------------------------------------------------
# DragImage Implementation
# This Class Handles The Creation Of A Custom Image In Case Of Item Drag
# And Drop.
#---------------------------------------------------------------------------

class DragImage(wx.DragImage):
    """
    This class handles the creation of a custom image in case of item drag
    and drop.
    """

    def __init__(self, treeCtrl, item):
        """
        Default class constructor.
        For internal use: do not call it in your code!

        :param `treeCtrl`: the parent :class:`CustomTreeCtrl`;
        :param `item`: one of the tree control item (an instance of :class:`GenericTreeItem`).
        """

        text = item.GetText()
        font = item.Attr().GetFont()
        colour = item.Attr().GetTextColour()
        if not colour:
            colour = wx.BLACK
        if not font:
            font = treeCtrl._normalFont

        backcolour = treeCtrl.GetBackgroundColour()
        r, g, b = int(backcolour.Red()), int(backcolour.Green()), int(backcolour.Blue())
        backcolour = ((r >> 1) + 20, (g >> 1) + 20, (b >> 1) + 20)
        backcolour = wx.Colour(backcolour[0], backcolour[1], backcolour[2])
        self._backgroundColour = backcolour

        tempdc = wx.ClientDC(treeCtrl)
        tempdc.SetFont(font)
        width, height, dummy = tempdc.GetFullMultiLineTextExtent(text + "M")

        image = item.GetCurrentImage()

        image_w, image_h = 0, 0
        wcheck, hcheck = 0, 0
        itemcheck = None
        itemimage = None
        ximagepos = 0
        yimagepos = 0
        xcheckpos = 0
        ycheckpos = 0

        if image != _NO_IMAGE:
            if treeCtrl._imageListNormal:
                image_w, image_h = treeCtrl._imageListNormal.GetSize(image)
                image_w += 4
                itemimage = treeCtrl._imageListNormal.GetBitmap(image)

        checkimage = item.GetCurrentCheckedImage()

        if checkimage is not None:
            if treeCtrl._imageListCheck:
                wcheck, hcheck = treeCtrl._imageListCheck.GetSize(checkimage)
                wcheck += 4
                itemcheck = treeCtrl._imageListCheck.GetBitmap(checkimage)

        total_h = max(hcheck, height)
        total_h = max(image_h, total_h)

        if image_w:
            ximagepos = wcheck
            yimagepos = ((total_h > image_h) and [(total_h-image_h)//2] or [0])[0]

        if checkimage is not None:
            xcheckpos = 2
            ycheckpos = ((total_h > image_h) and [(total_h-image_h)//2] or [0])[0] + 2

        extraH = ((total_h > height) and [(total_h - height)//2] or [0])[0]

        xtextpos = wcheck + image_w
        ytextpos = extraH

        total_h = max(image_h, hcheck)
        total_h = max(total_h, height)

        if total_h < 30:
            total_h += 2            # at least 2 pixels
        else:
            total_h += total_h//10   # otherwise 10% extra spacing

        total_w = image_w + wcheck + width

        self._total_w = total_w
        self._total_h = total_h
        self._itemimage = itemimage
        self._itemcheck = itemcheck
        self._text = text
        self._colour = colour
        self._font = font
        self._xtextpos = xtextpos
        self._ytextpos = ytextpos
        self._ximagepos = ximagepos
        self._yimagepos = yimagepos
        self._xcheckpos = xcheckpos
        self._ycheckpos = ycheckpos
        self._textwidth = width
        self._textheight = height
        self._extraH = extraH

        self._bitmap = self.CreateBitmap()

        wx.DragImage.__init__(self, self._bitmap)


    def CreateBitmap(self):
        """
        Actually creates the drag and drop bitmap for :class:`DragImage`.

        :return: An instance of :class:`DragImage`, a close representation of the item's
         appearance (i.e., a screenshot of the item).
        """

        memory = wx.MemoryDC()

        bitmap = wx.Bitmap(self._total_w, self._total_h)
        memory.SelectObject(bitmap)

        if wx.Platform == '__WXMAC__':
            memory.SetBackground(wx.TRANSPARENT_BRUSH)
        else:
            memory.SetBackground(wx.Brush(self._backgroundColour))
        memory.SetBackgroundMode(wx.TRANSPARENT)
        memory.SetFont(self._font)
        memory.SetTextForeground(self._colour)
        memory.Clear()

        if self._itemimage:
            memory.DrawBitmap(self._itemimage, self._ximagepos, self._yimagepos, True)

        if self._itemcheck:
            memory.DrawBitmap(self._itemcheck, self._xcheckpos, self._ycheckpos, True)

        textrect = wx.Rect(self._xtextpos, self._ytextpos+self._extraH, self._textwidth, self._textheight)
        memory.DrawLabel(self._text, textrect)

        memory.SelectObject(wx.NullBitmap)

        # Gtk and Windows unfortunately don't do so well with transparent
        # drawing so this hack corrects the image to have a transparent
        # background.
        if wx.Platform != '__WXMAC__':
            timg = bitmap.ConvertToImage()
            if not timg.HasAlpha():
                timg.InitAlpha()
            for y in range(timg.GetHeight()):
                for x in range(timg.GetWidth()):
                    pix = wx.Colour(timg.GetRed(x, y),
                                    timg.GetGreen(x, y),
                                    timg.GetBlue(x, y))
                    if pix == self._backgroundColour:
                        timg.SetAlpha(x, y, 0)
            bitmap = timg.ConvertToBitmap()
        return bitmap


# ----------------------------------------------------------------------------
# TreeItemAttr: a structure containing the visual attributes of an item
# ----------------------------------------------------------------------------

class TreeItemAttr(object):
    """
    Creates the item attributes (text colour, background colour and font).

    :note: This class is inspired by the wxWidgets generic implementation of :class:`TreeItemAttr`.
    """

    def __init__(self, colText=wx.NullColour, colBack=wx.NullColour, colBorder=wx.NullColour,font=wx.NullFont):
        """
        Default class constructor.
        For internal use: do not call it in your code!

        :param `colText`: the text colour, an instance of :class:`wx.Colour`;
        :param `colBack`: the tree item background colour, an instance of :class:`wx.Colour`;
        :param `colBorder`: the tree item border colour, an instance of :class:`wx.Colour`;
        :param `font`: the tree item font, an instance of :class:`wx.Font`.
        """

        self._colText = colText
        self._colBack = colBack
        self._colBorder = colBorder
        self._font = font

    # setters
    def SetTextColour(self, colText):
        """
        Sets the text colour attribute.

        :param `colText`: an instance of :class:`wx.Colour`.
        """

        self._colText = wx.Colour(colText)


    def SetBackgroundColour(self, colBack):
        """
        Sets the item background colour attribute.

        :param `colBack`: an instance of :class:`wx.Colour`.
        """

        self._colBack = wx.Colour(colBack)


    def SetBorderColour(self, colBorder):
        """
        Sets the item border colour attribute.

        :param `colBack`: an instance of :class:`wx.Colour`.

        .. versionadded:: 0.9.6
        """

        self._colBorder = wx.Colour(colBorder)


    def SetFont(self, font):
        """
        Sets the item font attribute.

        :param `font`: an instance of :class:`wx.Font`.
        """

        self._font = font


    # accessors
    def HasTextColour(self):
        """
        Returns whether the attribute has text colour.

        :return: ``True`` if the text colour attribute has been set, ``False`` otherwise.
        """

        return self._colText != wx.NullColour and self._colText.IsOk()


    def HasBackgroundColour(self):
        """
        Returns whether the attribute has background colour.

        :return: ``True`` if the background colour attribute has been set, ``False`` otherwise.
        """

        return self._colBack != wx.NullColour and self._colBack.IsOk()


    def HasBorderColour(self):
        """
        Returns whether the attribute has border colour.

        :return: ``True`` if the border colour attribute has been set, ``False`` otherwise.

        .. versionadded:: 0.9.6
        """

        return self._colBorder != wx.NullColour and self._colBorder.IsOk()


    def HasFont(self):
        """
        Returns whether the attribute has font.

        :return: ``True`` if the font attribute has been set, ``False`` otherwise.
        """

        return self._font != wx.NullFont and self._font.IsOk()


    # getters
    def GetTextColour(self):
        """
        Returns the attribute text colour.

        :return: An instance of :class:`wx.Colour`.
        """

        return self._colText


    def GetBackgroundColour(self):
        """
        Returns the attribute background colour.

        :return: An instance of :class:`wx.Colour`.
        """

        return self._colBack


    def GetBorderColour(self):
        """
        Returns the attribute border colour.

        :return: An instance of :class:`wx.Colour`.

        .. versionadded:: 0.9.6
        """

        return self._colBorder


    def GetFont(self):
        """
        Returns the attribute font.

        :return: An instance of :class:`wx.Font`.
        """

        return self._font


# ----------------------------------------------------------------------------
# CommandTreeEvent Is A Special Subclassing Of wx.CommandEvent
#
# NB: Note That Not All The Accessors Make Sense For All The Events, See The
# Event Description Below.
# ----------------------------------------------------------------------------

class CommandTreeEvent(wx.CommandEvent):
    """
    :class:`CommandTreeEvent` is a special subclassing of :class:`CommandEvent`.

    :note: Not all the accessors make sense for all the events, see the event description for every method in this class.
    """

    def __init__(self, evtType, evtId, item=None, evtKey=None, point=None,
                 label=None, **kwargs):
        """
        Default class constructor.
        For internal use: do not call it in your code!

        :param integer `evtType`: the event type;
        :param integer `evtId`: the event identifier;
        :param `item`: an instance of :class:`GenericTreeItem`;
        :param integer `evtKey`: a character ordinal;
        :param `point`: an instance of :class:`wx.Point`;
        :param string `label`: a :class:`GenericTreeItem` text label.
        """

        wx.CommandEvent.__init__(self, evtType, evtId, **kwargs)
        self._item = item
        self._evtKey = evtKey
        self._pointDrag = point
        self._label = label


    def GetItem(self):
        """
        Gets the item on which the operation was performed or the newly selected
        item for ``EVT_TREE_SEL_CHANGED`` and ``EVT_TREE_SEL_CHANGING`` events.

        :return: An instance of :class:`GenericTreeItem`.
        """

        return self._item


    def SetItem(self, item):
        """
        Sets the item on which the operation was performed or the newly selected
        item for ``EVT_TREE_SEL_CHANGED`` and ``EVT_TREE_SEL_CHANGING`` events.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        self._item = item


    def GetOldItem(self):
        """
        Returns the previously selected item for ``EVT_TREE_SEL_CHANGED`` and
        ``EVT_TREE_SEL_CHANGING`` events.

        :return: An instance of :class:`GenericTreeItem`.
        """

        return self._itemOld


    def SetOldItem(self, item):
        """
        Returns the previously selected item for ``EVT_TREE_SEL_CHANGED`` and
        ``EVT_TREE_SEL_CHANGING`` events.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        self._itemOld = item


    def GetPoint(self):
        """
        Returns the point where the mouse was when the drag operation started
        (for ``EVT_TREE_BEGIN_DRAG`` and ``EVT_TREE_BEGIN_RDRAG`` events only)
        or the click position.

        :return: An instance of :class:`wx.Point`.
        """

        return self._pointDrag


    def SetPoint(self, pt):
        """
        Sets the point where the mouse was when the drag operation started
        (for ``EVT_TREE_BEGIN_DRAG`` and ``EVT_TREE_BEGIN_RDRAG`` events only)
        or the click position.

        :param `pt`: an instance of :class:`wx.Point`.
        """

        self._pointDrag = pt


    def GetKeyEvent(self):
        """
        Returns the keyboard data (for ``EVT_TREE_KEY_DOWN`` event only).

        :return: An instance of :class:`KeyEvent`.
        """

        return self._evtKey


    def GetKeyCode(self):
        """
        Returns the virtual key code. ASCII events return normal ASCII values, while
        non-ASCII events return values such as ``wx.WXK_LEFT`` for the left cursor key.

        This method is for ``EVT_TREE_KEY_DOWN`` events only.

        :return: An integer representing the virtual key code.

        :note: In Unicode build, the returned value is meaningful only if the user entered
         a character that can be represented in current locale's default charset. You can
         obtain the corresponding Unicode character using `GetUnicodeKey`.
        """

        return self._evtKey.GetKeyCode()


    def SetKeyEvent(self, event):
        """
        Sets the keyboard data (for ``EVT_TREE_KEY_DOWN`` event only).

        :param `event`: a :class:`CommandTreeEvent` event to be processed.
        """

        self._evtKey = event


    def GetLabel(self):
        """
        Returns the item text (for ``EVT_TREE_BEGIN_LABEL_EDIT`` and
        ``EVT_TREE_END_LABEL_EDIT`` events only).

        :return: A string containing the item text.
        """

        return self._label


    def SetLabel(self, label):
        """
        Sets the item text (for ``EVT_TREE_BEGIN_LABEL_EDIT`` and
        ``EVT_TREE_END_LABEL_EDIT`` events only).

        :param string `label`: a string containing the new item text.
        """

        self._label = label


    def IsEditCancelled(self):
        """
        Returns the edit cancel flag (for ``EVT_TREE_BEGIN_LABEL_EDIT`` and
        ``EVT_TREE_END_LABEL_EDIT`` events only).

        :return: ``True`` is the item editing has been cancelled, ``False`` otherwise.
        """

        return self._editCancelled


    def SetEditCanceled(self, editCancelled):
        """
        Sets the edit cancel flag (for ``EVT_TREE_BEGIN_LABEL_EDIT`` and
        ``EVT_TREE_END_LABEL_EDIT`` events only).

        :param bool `editCancelled`: ``True`` to cancel the editing, ``False`` otherwise.
        """

        self._editCancelled = editCancelled


    def SetToolTip(self, toolTip):
        """
        Sets the tooltip for the item (for ``EVT_TREE_ITEM_GETTOOLTIP`` events).

        :param string `tooltip`: a string representing the item tooltip.
        """

        self._label = toolTip


    def GetToolTip(self):
        """
        Returns the tooltip for the item (for ``EVT_TREE_ITEM_GETTOOLTIP`` events).

        :return: A string containing the item tooltip.
        """

        return self._label


# ----------------------------------------------------------------------------
# TreeEvent is a special class for all events associated with tree controls
#
# NB: note that not all accessors make sense for all events, see the event
#     descriptions below
# ----------------------------------------------------------------------------

class TreeEvent(CommandTreeEvent):
    """
    :class:`CommandTreeEvent` is a special class for all events associated with tree controls.

    :note: Not all accessors make sense for all events, see the event descriptions below.
    """
    def __init__(self, evtType, evtId, item=None, evtKey=None, point=None,
                 label=None, **kwargs):
        """
        Default class constructor.
        For internal use: do not call it in your code!

        :param integer `evtType`: the event type;
        :param integer `evtId`: the event identifier;
        :param `item`: an instance of :class:`GenericTreeItem`;
        :param integer `evtKey`: a character ordinal;
        :param `point`: an instance of :class:`wx.Point`;
        :param string `label`: a :class:`GenericTreeItem` text label.
        """

        CommandTreeEvent.__init__(self, evtType, evtId, item, evtKey, point, label, **kwargs)
        self.notify = wx.NotifyEvent(evtType, evtId)


    def GetNotifyEvent(self):
        """
        Returns the actual :class:`NotifyEvent`.

        :return: An instance of :class:`NotifyEvent`.
        """

        return self.notify


    def IsAllowed(self):
        """
        Returns ``True`` if the change is allowed (:meth:`~TreeEvent.Veto` hasn't been called) or
        ``False`` otherwise (if it was).
        """

        return self.notify.IsAllowed()


    def Veto(self):
        """
        Prevents the change announced by this event from happening.

        :note: It is in general a good idea to notify the user about the reasons
         for vetoing the change because otherwise the applications behaviour (which
         just refuses to do what the user wants) might be quite surprising.
        """

        self.notify.Veto()


    def Allow(self):
        """
        This is the opposite of :meth:`~TreeEvent.Veto`: it explicitly allows the event to be processed.
        For most events it is not necessary to call this method as the events are
        allowed anyhow but some are forbidden by default (this will be mentioned
        in the corresponding event description).
        """

        self.notify.Allow()


# -----------------------------------------------------------------------------
# Auxiliary Classes: TreeEditTimer
# -----------------------------------------------------------------------------

class TreeEditTimer(wx.Timer):
    """ Timer used for enabling in-place edit."""

    def __init__(self, owner):
        """
        Default class constructor.
        For internal use: do not call it in your code!

        :param `owner`: the :class:`Timer` owner (an instance of :class:`CustomTreeCtrl`).
        """

        wx.Timer.__init__(self)
        self._owner = owner


    def Notify(self):
        """ The timer has expired, starts the item editing. """

        self._owner.OnEditTimer()


# -----------------------------------------------------------------------------
# Auxiliary Classes: TreeTextCtrl
# This Is The Temporary ExpandoTextCtrl Created When You Edit The Text Of An Item
# -----------------------------------------------------------------------------

class TreeTextCtrl(ExpandoTextCtrl):
    """
    Control used for in-place edit.

    This is a subclass of :class:`lib.expando.ExpandoTextCtrl` as :class:`CustomTreeCtrl` supports multiline
    text items.

    :note: To add a newline character in a multiline item, press ``Shift`` + ``Enter`` as the ``Enter``
     key alone is consumed by :class:`CustomTreeCtrl` to finish the editing and ``Ctrl`` + ``Enter`` is
     consumed by the platform for tab navigation.
    """

    def __init__(self, owner, item=None):
        """
        Default class constructor.
        For internal use: do not call it in your code!

        :param `owner`: the control parent (an instance of :class:`CustomTreeCtrl`);
        :param `item`: an instance of :class:`GenericTreeItem`.

        :raise: `Exception` when the item has an associated image but the parent
         :class:`CustomTreeCtrl` does not have a :class:`wx.ImageList` assigned.
        """

        self._owner = owner
        self._itemEdited = item
        self._startValue = item.GetText()
        self._finished = False
        self._aboutToFinish = False
        self._currentValue = self._startValue

        w = self._itemEdited.GetWidth()
        h = self._itemEdited.GetHeight()

        wnd = self._itemEdited.GetWindow()
        if wnd:
            w = w - self._itemEdited.GetWindowSize()[0]
            h = 0

        x, y = self._owner.CalcScrolledPosition(item.GetX(), item.GetY())

        image_h = 0
        image_w = 0

        image = item.GetCurrentImage()

        if image != _NO_IMAGE:

            if self._owner._imageListNormal:
                image_w, image_h = self._owner._imageListNormal.GetSize(image)
                image_w += 4

            else:

                raise Exception("\n ERROR: You Must Create An Image List To Use Images!")

        checkimage = item.GetCurrentCheckedImage()

        if checkimage is not None:
            wcheck, hcheck = self._owner._imageListCheck.GetSize(checkimage)
            wcheck += 4
        else:
            wcheck = hcheck = 0

        if wnd:
            h = max(hcheck, image_h)
            dc = wx.ClientDC(self._owner)
            h = max(h, dc.GetTextExtent("Aq")[1])
            h = h + 2

        # FIXME: what are all these hardcoded 4, 8 and 11s really?
        x += image_w + wcheck
        w -= image_w + 4 + wcheck

        expandoStyle = wx.WANTS_CHARS
        if wx.Platform in ["__WXGTK__", "__WXMAC__"]:
            expandoStyle |= wx.SIMPLE_BORDER
            xSize, ySize = w + 25, h
        else:
            expandoStyle |= wx.SUNKEN_BORDER
            xSize, ySize = w + 25, h+2

        ExpandoTextCtrl.__init__(self, self._owner, wx.ID_ANY, self._startValue,
                                 wx.Point(x - 4, y), wx.Size(xSize, ySize),
                                 expandoStyle)

        if wx.Platform == "__WXMAC__":
            self.SetFont(owner.GetFont())
            bs = self.GetBestSize()
            self.SetSize((-1, bs.height))

        if self._startValue:
            self.SelectAll()
          
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)


    def AcceptChanges(self):
        """
        Accepts/rejects the changes made by the user.

        :return: ``True`` if the changes to the item text have been accepted, ``False``
         if they have been rejected (i.e., vetoed by the user).
        """

        value = self.GetValue()

        if value == self._startValue:
            # nothing changed, always accept
            # when an item remains unchanged, the owner
            # needs to be notified that the user decided
            # not to change the tree item label, and that
            # the edit has been cancelled
            self._owner.OnCancelEdit(self._itemEdited)
            return True

        if not self._owner.OnAcceptEdit(self._itemEdited, value):
            # vetoed by the user
            return False

        # accepted, do rename the item
        self._owner.SetItemText(self._itemEdited, value)

        return True


    def Finish(self):
        """ Finish editing. """

        if not self._finished:
            self._finished = True
            self._owner.SetFocusIgnoringChildren()
            self._owner.ResetEditControl()


    def OnChar(self, event):
        """
        Handles the ``wx.EVT_CHAR`` event for :class:`TreeTextCtrl`.

        :param `event`: a :class:`KeyEvent` event to be processed.
        """

        keycode = event.GetKeyCode()
        shiftDown = event.ShiftDown()

        if keycode in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
            if shiftDown:
                event.Skip()
            else:
                self._aboutToFinish = True
                self.SetValue(self._currentValue)
                # Notify the owner about the changes
                self.AcceptChanges()
                # Even if vetoed, close the control (consistent with MSW)
                wx.CallAfter(self.Finish)

        elif keycode == wx.WXK_ESCAPE:
            self.StopEditing()

        else:
            event.Skip()


    def OnKeyUp(self, event):
        """
        Handles the ``wx.EVT_KEY_UP`` event for :class:`TreeTextCtrl`.

        :param `event`: a :class:`KeyEvent` event to be processed.
        """

        if not self._finished:

            # auto-grow the textctrl:
            parentSize = self._owner.GetSize()
            myPos = self.GetPosition()
            mySize = self.GetSize()

            dc = wx.ClientDC(self)
            sx, sy, dummy = dc.GetFullMultiLineTextExtent(self.GetValue() + "M")

            if myPos.x + sx > parentSize.x:
                sx = parentSize.x - myPos.x
            if mySize.x > sx:
                sx = mySize.x

            self.SetSize((sx, -1))
            self._currentValue = self.GetValue()

        event.Skip()


    def OnKillFocus(self, event):
        """
        Handles the ``wx.EVT_KILL_FOCUS`` event for :class:`TreeTextCtrl`.

        :param `event`: a :class:`FocusEvent` event to be processed.
        """

        if not self._finished and not self._aboutToFinish:

            # We must finish regardless of success, otherwise we'll get
            # focus problems:

            if not self.AcceptChanges():
                self._owner.OnCancelEdit(self._itemEdited)

        # We must let the native text control handle focus, too, otherwise
        # it could have problems with the cursor (e.g., in wxGTK).
        event.Skip()


    def StopEditing(self):
        """ Suddenly stops the editing. """

        self._owner.OnCancelEdit(self._itemEdited)
        self.Finish()


    def item(self):
        """
        Returns the item currently edited.

        :return: An instance of :class:`GenericTreeItem`.
        """

        return self._itemEdited


# -----------------------------------------------------------------------------
# Auxiliary Classes: TreeFindTimer
# Timer Used To Clear CustomTreeCtrl._findPrefix If No Key Was Pressed For A
# Sufficiently Long Time.
# -----------------------------------------------------------------------------

class TreeFindTimer(wx.Timer):
    """
    Timer used to clear the :class:`CustomTreeCtrl` `_findPrefix` attribute if no
    key was pressed for a sufficiently long time.
    """

    def __init__(self, owner):
        """
        Default class constructor.
        For internal use: do not call it in your code!

        :param `owner`: the :class:`Timer` owner (an instance of :class:`CustomTreeCtrl`).
        """

        wx.Timer.__init__(self)
        self._owner = owner


    def Notify(self):
        """ The timer has expired, clear the `_findPrefix` attribute in :class:`CustomTreeCtrl`. """

        self._owner._findPrefix = ""


# -----------------------------------------------------------------------------
# GenericTreeItem Implementation.
# This Class Holds All The Information And Methods For Every Single Item In
# CustomTreeCtrl.
# -----------------------------------------------------------------------------

class GenericTreeItem(object):
    """
    This class holds all the information and methods for every single item in
    :class:`CustomTreeCtrl`. This is a generic implementation of :class:`TreeItem`.
    """

    def __init__(self, parent, text="", ct_type=0, wnd=None, image=-1, selImage=-1, data=None, separator=False, on_the_right=True):
        """
        Default class constructor.
        For internal use: do not call it in your code!

        :param `parent`: the tree item parent, an instance of :class:`GenericTreeItem` (may
         be ``None`` for root items);
        :param string `text`: the tree item text;
        :param integer `ct_type`: the tree item kind. May be one of the following integers:

         =============== =========================================
         `ct_type` Value Description
         =============== =========================================
                0        A normal item
                1        A checkbox-like item
                2        A radiobutton-type item
         =============== =========================================

        :param `wnd`: if not ``None``, a non-toplevel window to be displayed next to
         the item, an instance of :class:`wx.Window`;
        :param integer `image`: an index within the normal image list specifying the image to
         use for the item in unselected state;
        :param integer `selImage`: an index within the normal image list specifying the image to
         use for the item in selected state; if `image` > -1 and `selImage` is -1, the
         same image is used for both selected and unselected items;
        :param object `data`: associate the given Python object `data` with the item;
        :param bool `separator`: ``True`` if the item is a separator, ``False`` otherwise.
        :param bool `on_the_right`: ``True`` positions the window on the right of text, ``False``
         on the left of text and overlapping the image.

        :note: Regarding radiobutton-type items (with `ct_type` = 2), the following
         approach is used:

         - All peer-nodes that are radiobuttons will be mutually exclusive. In other words,
           only one of a set of radiobuttons that share a common parent can be checked at
           once. If a radiobutton node becomes checked, then all of its peer radiobuttons
           must be unchecked.
         - If a radiobutton node becomes unchecked, then all of its child nodes will become
           inactive.


        :note: Separator items should not have children, labels, data or an associated window.
         Other issues/features associated to separator items:

         - You can change the color of individual separators by using :meth:`CustomTreeCtrl.SetItemTextColour() <customtreectrl.CustomTreeCtrl.SetItemTextColour>`,
           or you can use :meth:`CustomTreeCtrl.SetSeparatorColour() <customtreectrl.CustomTreeCtrl.SetSeparatorColour>` to change the color of all
           separators. The default separator colour is that returned by `SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)`;
         - Separators can be selected just like any other tree item;
         - Separators cannot have text;
         - Separators cannot have children;
         - Separators cannot be edited via the ``EVT_TREE_BEGIN_LABEL_EDIT`` event.

        """

        # since there can be very many of these, we save size by choosing
        # the smallest representation for the elements and by ordering
        # the members to avoid padding.
        self._text = text       # label to be rendered for item
        self._data = data       # user-provided data

        self._children  = []    # list of children
        self._parent = parent   # parent of this item

        self._attr = None       # attributes???

        self._separator = separator

        # tree ctrl images for the normal, selected, expanded and
        # expanded+selected states
        self._images = [-1, -1, -1, -1]
        self._images[TreeItemIcon_Normal] = image
        self._images[TreeItemIcon_Selected] = selImage
        self._images[TreeItemIcon_Expanded] = _NO_IMAGE
        self._images[TreeItemIcon_SelectedExpanded] = _NO_IMAGE

        self._checkedimages = [None, None, None, None, None]
        self._leftimage = _NO_IMAGE

        self._x = 0             # (virtual) offset from top
        self._y = 0             # (virtual) offset from left
        self._width = 0         # width of this item
        self._height = 0        # height of this item

        self._isCollapsed = True
        self._hasHilight = False    # same as focused
        self._hasPlus = False       # used for item which doesn't have
                                    # children but has a [+] button
        self._isBold = False        # render the label in bold font
        self._isItalic = False      # render the label in italic font
        self._ownsAttr = False      # delete attribute when done
        self._type = ct_type        # item type: 0=normal, 1=check, 2=radio
        self._is3State = False      # true for 3-state checkbox items
        self._checked = False       # only meaningful for check and radio items
        self._enabled = True        # flag to enable/disable an item
        self._hypertext = False     # indicates if the item is hypertext
        self._visited = False       # visited state for an hypertext item
        self._hidden = False        # hidden items are not painted

        if self._type > 0:
            # do not construct the array for normal items
            self._checkedimages[TreeItemIcon_Checked] = 0
            self._checkedimages[TreeItemIcon_NotChecked] = 1
            self._checkedimages[TreeItemIcon_Undetermined] = 2
            self._checkedimages[TreeItemIcon_Flagged] = 3
            self._checkedimages[TreeItemIcon_NotFlagged] = 4

        if parent:
            if parent.GetType() == 2 and not parent.IsChecked():
                # if the node parent is a radio not enabled, we are disabled
                self._enabled = False

        self._wnd = wnd             # are we holding a window?
        self._windowontheright = on_the_right  # on the right, or left?

        if wnd:
            self.SetWindow(wnd, on_the_right)


    def IsOk(self):
        """
        Returns whether the item is ok or not.

        :note: This method always returns ``True``, it has been added for
         backward compatibility with the wxWidgets C++ implementation.
        """

        return True


    def IsSeparator(self):
        """
        Returns whether the item is meant to be an horizontal line separator or not.

        :return: ``True`` if this item is a separator, ``False`` otherwise.
        """

        return self._separator


    def GetChildren(self):
        """
        Returns the item's children.

        :return: A Python list containing instances of :class:`GenericTreeItem`, representing
         this item's children.
         
        :note: The returned value is a reference to the list of children
         used internally by the tree. It is advised not to change this list
         and to make a copy before calling other tree methods as they could
         change the contents of the list.
        """

        return self._children


    def GetText(self):
        """
        Returns the item text.

        :return: A string containing the item text.
        """

        return self._text


    def GetImage(self, which=TreeItemIcon_Normal):
        """
        Returns the item image for a particular item state.

        :param integer `which`: can be one of the following bits:

         ================================= ========================
         Item State                        Description
         ================================= ========================
         ``TreeItemIcon_Normal``           To get the normal item image
         ``TreeItemIcon_Selected``         To get the selected item image (i.e. the image which is shown when the item is currently selected)
         ``TreeItemIcon_Expanded``         To get the expanded image (this only makes sense for items which have children - then this image is shown when the item is expanded and the normal image is shown when it is collapsed)
         ``TreeItemIcon_SelectedExpanded`` To get the selected expanded image (which is shown when an expanded item is currently selected)
         ================================= ========================

        :return: An integer index that can be used to retrieve the item image inside
         a :class:`wx.ImageList`.
        """

        return self._images[which]


    def GetCheckedImage(self, which=TreeItemIcon_Checked):
        """
        Returns the item check image.

        :param integer `which`: can be one of the following bits:

         ================================= ========================
         Item State                        Description
         ================================= ========================
         ``TreeItemIcon_Checked``          To get the checkbox checked item image
         ``TreeItemIcon_NotChecked``       To get the checkbox unchecked item image
         ``TreeItemIcon_Undetermined``     To get the checkbox undetermined state item image
         ``TreeItemIcon_Flagged``          To get the radiobutton checked image
         ``TreeItemIcon_NotFlagged``       To get the radiobutton unchecked image
         ================================= ========================

        :return: An integer index that can be used to retrieve the item check image inside
         a :class:`wx.ImageList`.

        :note: This method is meaningful only for radio & check items.
        """

        return self._checkedimages[which]


    def GetLeftImage(self):
        """
        Returns the leftmost image associated to this item, i.e. the image on the
        leftmost part of the client area of :class:`CustomTreeCtrl`.

        :return: An integer index that can be used to retrieve the item leftmost image inside
         a :class:`wx.ImageList`.
        """

        return self._leftimage


    def GetData(self):
        """
        Returns the data associated to this item.

        :return: A Python object representing the item data, or ``None`` if no data
         has been assigned to this item.
        """

        return self._data


    def SetImage(self, image, which):
        """
        Sets the item image.

        :param integer `image`: an index within the normal image list specifying the image to use;
        :param integer `which`: the image kind.

        :see: :meth:`~GenericTreeItem.GetImage` for a description of the `which` parameter.
        
        :note: Call :meth:`CustomTreeCtrl.SetItemImage` instead to refresh the tree properly.
        """

        self._images[which] = image


    def SetLeftImage(self, image):
        """
        Sets the item leftmost image, i.e. the image associated to the item on the leftmost
        part of the :class:`CustomTreeCtrl` client area.

        :param integer `image`: an index within the left image list specifying the image to
         use for the item in the leftmost part of the client area.
         
        :note: Call :meth:`CustomTreeCtrl.SetItemLeftImage` instead to refresh the tree properly.
        """

        self._leftimage = image


    def SetData(self, data):
        """
        Sets the data associated to this item.

        :param object `data`: can be any Python object.
        """

        self._data = data


    def SetHasPlus(self, has=True):
        """
        Sets whether an item has the 'plus' button.

        :param bool `has`: ``True`` to set the 'plus' button on the item, ``False`` otherwise.
        
        :note: Call :meth:`CustomTreeCtrl.SetItemHasChildren` instead to refresh the tree properly.
        """

        self._hasPlus = has


    def SetBold(self, bold):
        """
        Sets the item font bold.

        :parameter bool `bold`: ``True`` to have a bold font item, ``False`` otherwise.
        
        :note: Call :meth:`CustomTreeCtrl.SetItemBold` instead to refresh the tree properly.
        """

        self._isBold = bold


    def SetItalic(self, italic):
        """
        Sets the item font italic.

        :parameter bool `italic`: ``True`` to have an italic font item, ``False`` otherwise.
        
        :note: Call :meth:`CustomTreeCtrl.SetItemItalic` instead to refresh the tree properly.
        """

        self._isItalic = italic


    def GetX(self):
        """ Returns the `x` position on an item, in logical coordinates. """

        return self._x


    def GetY(self):
        """ Returns the `y` position on an item, in logical coordinates. """

        return self._y


    def SetX(self, x):
        """
        Sets the `x` position on an item, in logical coordinates.

        :param integer `x`: an integer specifying the x position of the item.
        """

        self._x = x


    def SetY(self, y):
        """
        Sets the `y` position on an item, in logical coordinates.

        :param integer `y`: an integer specifying the y position of the item.
        """

        self._y = y


    def GetHeight(self):
        """ Returns the height of the item, in pixels.

        This will be 0 when the item is first created and always 0 for hidden
        items. It is updated when the item is calculated.
        """

        return self._height


    def GetWidth(self):
        """ Returns the width of the item's contents, in pixels.

        This is the width of the item's text plus the widths of the item's
        image, checkbox, and window (if they exist).
        A separator's width is the width of the entire client area.
        """

        return self._width


    def SetHeight(self, h):
        """
        Sets the item's height. Used internally.

        :param integer `h`: an integer specifying the item's height, in pixels.
        """

        self._height = h


    def SetWidth(self, w):
        """
        Sets the item's width. Used internally.

        :param integer `w`: an integer specifying the item's width, in pixels.
        """

        self._width = w


    def SetWindow(self, wnd, on_the_right=True):
        """
        Sets the window associated to the item. Internal use only.

        :param `wnd`: a non-toplevel window to be displayed next to the item, any
         subclass of :class:`wx.Window`.

        :param bool `on_the_right`: ``True`` positions the window on the right of text, ``False``
         on the left of text and overlapping the image. New in wxPython 4.0.4.

        :raise: `Exception` if the input `item` is a separator and `wnd` is not ``None``.
        
        :note: Always use :meth:`CustomTreeCtrl.SetItemWindow` instead to update the tree properly.
        """

        if self.IsSeparator() and wnd is not None:
            raise Exception("Separator items can not have an associated window")

        self._wnd = wnd
        self._windowontheright = on_the_right

        if wnd.GetSizer():      # the window is a complex one hold by a sizer
            size = wnd.GetBestSize()
        else:                   # simple window, without sizers
            size = wnd.GetSize()

        # We have to bind the wx.EVT_SET_FOCUS for the associated window
        # No other solution to handle the focus changing from an item in
        # CustomTreeCtrl and the window associated to an item
        # Do better strategies exist?
        self._wnd.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)

        # We also have to bind the wx.EVT_TREE_ITEM_COLLAPSING for the
        # associated window, for example when it is an agw.animate.AnimationCtrl,
        # otherwise it would stay visible. See the demo for an example.
        self._wnd.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnTreeItemCollapsing)

        self._height = size.GetHeight() + 2
        self._width = size.GetWidth()
        self._windowsize = size

        ## Hide the window since the position isn't correct yet. It will
        ## be shown and positioned when the item is painted.
        wnd.Show(False)

        # The window is enabled only if the item is enabled
        self._wnd.Enable(self._enabled)
        self._windowenabled = self._enabled



    def GetWindow(self):
        """
        Returns the window associated to the item (if any).

        :return: An instance of any :class:`wx.Window` derived class, excluding top-level windows.
        """

        return self._wnd


    def DeleteWindow(self):
        """ Deletes the window associated to the item (if any). Internal use only.

        :note: Always use :meth:`CustomTreeCtrl.DeleteItemWindow` instead to update the tree properly.
        """

        if self._wnd:
            self._wnd.Destroy()
            self._wnd = None


    def GetWindowEnabled(self):
        """
        Returns whether the associated window is enabled or not.

        :return: ``True`` if the associated window is enabled, ``False`` if it is disabled.

        :raise: `Exception` when the item has no associated window.
        """

        if not self._wnd:
            raise Exception("\nERROR: This Item Has No Window Associated")

        return self._windowenabled


    def SetWindowEnabled(self, enable=True):
        """
        Sets whether the associated window is enabled or not.

        :param bool `enable`: ``True`` to enable the associated window, ``False`` to disable it.

        :raise: `Exception` when the item has no associated window.
        """

        if not self._wnd:
            raise Exception("\nERROR: This Item Has No Window Associated")

        self._windowenabled = enable
        self._wnd.Enable(enable)


    def GetWindowSize(self):
        """ Returns the associated window size. """

        return self._windowsize


    def OnSetFocus(self, event):
        """
        Handles the ``wx.EVT_SET_FOCUS`` event for the window associated with the item.

        :param `event`: a :class:`FocusEvent` event to be processed.
        """

        treectrl = self._wnd.GetParent()
        select = treectrl.GetSelection()

        # If the window is associated to an item that currently is selected
        # (has focus) we don't kill the focus. Otherwise we do it.
        if select != self:
            treectrl._hasFocus = False
        else:
            treectrl._hasFocus = True

        event.Skip()


    def OnTreeItemCollapsing(self, event):
        """
        Handles the ``wx.EVT_TREE_ITEM_COLLAPSING`` event for the window associated with the item.

        :param `event`: a :class:`GenericTreeItem` to be processed.
        """
        # Helio: This is not OK?
        #        Should it be more "internal" code?
        #        It is working on the user application.
        for item in event.GetItem().GetChildren():
            itemwindow = item.GetWindow()
            if itemwindow:  # Hides the attached window if added
                itemwindow.Hide()

        # Hides the attached window if added
        #if self._wnd:
        #    self._wnd.Hide()

        event.Skip()


    def GetType(self):
        """
        Returns the item type.

        :see: :meth:`~GenericTreeItem.SetType` and :meth:`~GenericTreeItem.__init__` for a description of valid item types.
        """

        return self._type


    def SetType(self, ct_type):
        """
        Sets the item type.

        :param integer `ct_type`: may be one of the following integers:

         =============== =========================================
         `ct_type` Value Description
         =============== =========================================
                0        A normal item
                1        A checkbox-like item
                2        A radiobutton-type item
         =============== =========================================

        :note: Regarding radiobutton-type items (with `ct_type` = 2), the following
         approach is used:

         - All peer-nodes that are radiobuttons will be mutually exclusive. In other words,
           only one of a set of radiobuttons that share a common parent can be checked at
           once. If a radiobutton node becomes checked, then all of its peer radiobuttons
           must be unchecked.
         - If a radiobutton node becomes unchecked, then all of its child nodes will become
           inactive.
           
        :note: Call :meth:`CustomTreeCtrl.SetItemType` instead to refresh the tree properly.
        """

        self._type = ct_type


    def SetHyperText(self, hyper=True):
        """
        Sets whether the item is hypertext or not.

        :param bool `hyper`: ``True`` to set hypertext behaviour, ``False`` otherwise.
        
        :note: Call :meth:`CustomTreeCtrl.SetItemHyperText` instead to refresh the tree properly.
        """

        self._hypertext = hyper


    def SetVisited(self, visited=True):
        """
        Sets whether an hypertext item was visited or not.

        :param bool `visited`: ``True`` to set a hypertext item as visited, ``False`` otherwise.
        
        :note: Call :meth:`CustomTreeCtrl.SetItemVisited` instead to refresh the tree properly.
        """

        self._visited = visited


    def GetVisited(self):
        """ Returns whether an hypertext item was visited or not. """

        return self._visited


    def IsHyperText(self):
        """ Returns whether the item is hypetext or not. """

        return self._hypertext


    def IsHidden(self):
        """ Returns whether the item is hidden or not. """

        return self._hidden


    def Hide(self, hide):
        """
        Hides/shows the item. Internal use only.

        :param `hide`: ``True`` to hide the item, ``False`` to show it.
        
        :note: Always use :meth:`CustomTreeCtrl.HideItem` instead to update the tree properly.
        """

        self._hidden = hide


    def GetParent(self):
        """
        Gets the item parent (another instance of :class:`GenericTreeItem` or ``None`` for
        root items.

        :return: An instance of :class:`GenericTreeItem` or ``None`` for root items.
        """

        return self._parent


    def Insert(self, child, index):
        """
        Inserts an item in the item children list for this item.

        :param `child`: an instance of :class:`GenericTreeItem`;
        :param integer `index`: the index at which we should insert the new child.
        """

        self._children.insert(index, child)


    def Expand(self):
        """ Expands the item. Internal use only.

        :note: Always use :meth:`CustomTreeCtrl.Expand` instead to update the tree properly and send events.
        """

        self._isCollapsed = False


    def Collapse(self):
        """ Collapses the item. Internal use only.

        :note: Always use :meth:`CustomTreeCtrl.Collapse` instead to update the tree properly and send events.
        """

        self._isCollapsed = True


    def SetHilight(self, set=True):
        """
        Sets the item focus/unfocus.

        :param bool `set`: ``True`` to set the focus to the item, ``False`` otherwise.
        
        :note: Call :meth:`CustomTreeCtrl.SelectItem` instead to update the tree properly and send events.
        """

        self._hasHilight = set


    def HasChildren(self):
        """
        Returns whether the item has children or not.

        :return: ``True`` if the item has children, ``False`` otherwise.
        """

        return len(self._children) > 0


    def IsSelected(self):
        """
        Returns whether the item is selected or not.

        :return: ``True`` if the item is selected, ``False`` otherwise.
        """

        return self._hasHilight != 0


    def IsExpanded(self):
        """
        Returns whether the item is expanded or not. Hidden items always return False.

        :return: ``True`` if the item is expanded, ``False`` if it is collapsed.
        """
        if self.IsHidden():
            return False
        return not self._isCollapsed


    def GetValue(self):
        """
        Returns whether the item is checked or not.

        :note: This is meaningful only for checkbox-like and radiobutton-like items.
        """

        if self.Is3State():
            return self.Get3StateValue()

        return self._checked


    def Get3StateValue(self):
        """
        Gets the state of a 3-state checkbox item.

        :return: ``wx.CHK_UNCHECKED`` when the checkbox is unchecked, ``wx.CHK_CHECKED``
         when it is checked and ``wx.CHK_UNDETERMINED`` when it's in the undetermined
         state.

        :raise: `Exception` when the item is not a 3-state checkbox item.

        :note: This method raises an exception when the function is used with a 2-state
         checkbox item.

        :note: This method is meaningful only for checkbox-like items.
        """

        if not self.Is3State():
            raise Exception("Get3StateValue can only be used with 3-state checkbox items.")

        return self._checked


    def Is3State(self):
        """
        Returns whether or not the checkbox item is a 3-state checkbox.

        :return: ``True`` if this checkbox is a 3-state checkbox, ``False`` if it's a
         2-state checkbox item.

        :note: This method is meaningful only for checkbox-like items.
        """

        return self._is3State


    def Set3StateValue(self, state):
        """
        Sets the checkbox item to the given `state`.

        :param integer `state`: can be one of: ``wx.CHK_UNCHECKED`` (check is off), ``wx.CHK_CHECKED``
         (check is on) or ``wx.CHK_UNDETERMINED`` (check is mixed).

        :raise: `Exception` when the item is not a 3-state checkbox item.

        :note: This method raises an exception when the checkbox item is a 2-state checkbox
         and setting the state to ``wx.CHK_UNDETERMINED``.

        :note: This method is meaningful only for checkbox-like items.
        """
        assert state in [wx.CHK_UNCHECKED, wx.CHK_CHECKED, wx.CHK_UNDETERMINED]
        if not self._is3State and state == wx.CHK_UNDETERMINED:
            raise Exception("Set3StateValue can only be used with 3-state checkbox items.")

        self._checked = state


    def Set3State(self, allow):
        """
        Sets whether the item has a 3-state value checkbox assigned to it or not.

        :param bool `allow`: ``True`` to set an item as a 3-state checkbox, ``False`` to set it
         to a 2-state checkbox.

        :return: ``True`` if the change was successful, ``False`` otherwise.

        :note: This method is meaningful only for checkbox-like items.
        """

        if self._type != 1:
            return False

        self._is3State = allow
        return True


    def IsChecked(self):
        """
        This is just a maybe more readable synonym for :meth:`~GenericTreeItem.GetValue`.
        Returns whether the item is checked or not.

        :note: This is meaningful only for checkbox-like and radiobutton-like items.
        """

        return self.GetValue()


    def Check(self, checked=True):
        """
        Checks/unchecks an item. Internal use only.

        :param bool `checked`: ``True`` to check an item, ``False`` to uncheck it.

        :note: This is meaningful only for checkbox-like and radiobutton-like items.
        
        :note: Always use :meth:`CustomTreeCtrl.CheckItem` instead to update the tree properly and send events.
        """
        assert checked in [True, False]
        self._checked = checked


    def HasPlus(self):
        """
        Returns whether the item has the plus button or not.

        :return: ``True`` if the item has a 'plus' mark, ``False`` otherwise.
        """

        return self._hasPlus or self.HasChildren()


    def IsBold(self):
        """
        Returns whether the item font is bold or not.

        :return: ``True`` if the item has bold text, ``False`` otherwise.
        """

        return self._isBold != 0


    def IsItalic(self):
        """
        Returns whether the item font is italic or not.

        :return: ``True`` if the item has italic text, ``False`` otherwise.
        """

        return self._isItalic != 0


    def Enable(self, enable=True):
        """
        Enables/disables the item.

        :param bool `enable`: ``True`` to enable the item, ``False`` to disable it.
        
        :note: Call :meth:`CustomTreeCtrl.EnableItem` instead to update the tree properly.
        """

        self._enabled = enable


    def IsEnabled(self):
        """
        Returns whether the item is enabled or not. Hidden items always return False.

        :return: ``True`` if the item is enabled, ``False`` if it is disabled.
        """
        if self.IsHidden():
            return False
        return self._enabled


    def GetAttributes(self):
        """
        Returns the item attributes (font, colours, etc...).

        :return: An instance of :class:`TreeItemAttr`.
        """

        return self._attr


    def Attr(self):
        """
        Creates a new attribute (font, colours, etc...) for this item.

        :return: An instance of :class:`TreeItemAttr`.
        """

        if not self._attr:

            self._attr = TreeItemAttr()
            self._ownsAttr = True

        return self._attr


    def SetAttributes(self, attr):
        """
        Sets the item attributes (font, colours, etc...).

        :param `attr`: an instance of :class:`TreeItemAttr`.
        """

        if self._ownsAttr:
             del self._attr

        self._attr = attr
        self._ownsAttr = False


    def AssignAttributes(self, attr):
        """
        Assigns the item attributes (font, colours, etc...) for this item.

        :param `attr`: an instance of :class:`TreeItemAttr`.
        """

        self.SetAttributes(attr)
        self._ownsAttr = True


    def DeleteChildren(self, tree):
        """
        Deletes the item children. Internal use only.

        :param `tree`: the main :class:`CustomTreeCtrl` instance.
        
        :note: Always use :meth:`CustomTreeCtrl.DeleteChildren` instead to update the tree properly.
        """

        for child in self._children:
            if tree:
                tree.SendDeleteEvent(child)

            child.DeleteChildren(tree)

            if child == tree._select_me:
                tree._select_me = None

            # We have to destroy the associated window
            wnd = child.GetWindow()
            if wnd:
                wnd.Destroy()
                child._wnd = None

            if child in tree._itemWithWindow:
                tree._itemWithWindow.remove(child)

            del child

        self._children = []


    def SetText(self, text):
        """
        Sets the item text.

        :param string `text`: the new item label.

        :raise: `Exception` if the item is a separator.
        
        :note: Call :meth:`CustomTreeCtrl.SetItemText` to refresh the tree properly.
        """

        if self.IsSeparator():
            raise Exception("Separator items can not have text")

        self._text = text


    def GetChildrenCount(self, recursively=True):
        """
        Gets the number of children of this item.

        :param bool `recursively`: if ``True``, returns the total number of descendants,
         otherwise only one level of children is counted.
        """

        count = len(self._children)

        if not recursively:
            return count

        total = count

        for n in range(count):
            total += self._children[n].GetChildrenCount()

        return total


    def GetSize(self, x, y, theButton):
        """
        Returns the item size.

        :param integer `x`: the current item's x position;
        :param integer `y`: the current item's y position;
        :param `theButton`: an instance of the main :class:`CustomTreeCtrl`.

        :return: A tuple of (`x`, `y`) dimensions, in pixels, representing the
         item's width and height.
        """

        bottomY = self._y + theButton.GetLineHeight(self)

        if y < bottomY:
            y = bottomY

        width = self._x + self._width

        if x < width:
            x = width

        if self.IsExpanded():
            for child in self._children:
                x, y = child.GetSize(x, y, theButton)

        return x, y


    def HitTest(self, point, theCtrl, flags=0, level=0):
        """
        :meth:`~GenericTreeItem.HitTest` method for an item. Called from the main window :meth:`CustomTreeCtrl.HitTest() <customtreectrl.CustomTreeCtrl.HitTest>`.

        :param `point`: the point to test for the hit (an instance of :class:`wx.Point`);
        :param `theCtrl`: the main :class:`CustomTreeCtrl` tree;
        :param integer `flags`: a bitlist of hit locations;
        :param integer `level`: the item's level inside the tree hierarchy.

        :see: :meth:`CustomTreeCtrl.HitTest() <customtreectrl.CustomTreeCtrl.HitTest>` method for the flags explanation.

        :return: A 2-tuple of (item, flags). The item may be ``None``.        
        """
        # Hidden items are never evaluated.
        if self.IsHidden():
            return None, flags

        # for a hidden root node, don't evaluate it, but do evaluate children
        if not (level == 0 and theCtrl.HasAGWFlag(TR_HIDE_ROOT)):

            # evaluate the item
            h = theCtrl.GetLineHeight(self)

            pointX, pointY = point[0], point[1]
            if pointY > self._y and pointY < self._y + h:

                y_mid = self._y + h//2

                if pointY < y_mid:
                    flags |= TREE_HITTEST_ONITEMUPPERPART
                else:
                    flags |= TREE_HITTEST_ONITEMLOWERPART

                xCross = self._x - theCtrl.GetSpacing()

                if wx.Platform == "__WXMAC__":
                    # according to the drawing code the triangels are drawn
                    # at -4 , -4  from the position up to +10/+10 max
                    if pointX > xCross-4 and pointX < xCross+10 and pointY > y_mid-4 and \
                       pointY < y_mid+10 and self.HasPlus() and theCtrl.HasButtons():

                        flags |= TREE_HITTEST_ONITEMBUTTON
                        return self, flags
                else:
                    # 5 is the size of the plus sign
                    if pointX > xCross-6 and pointX < xCross+6 and pointY > y_mid-6 and \
                       pointY < y_mid+6 and self.HasPlus() and theCtrl.HasButtons():

                        flags |= TREE_HITTEST_ONITEMBUTTON
                        return self, flags

                if pointX >= self._x and pointX <= self._x + self._width:

                    image_w = -1
                    wcheck = 0

                    # assuming every image (normal and selected) has the same size!
                    if self.GetImage() != _NO_IMAGE and theCtrl._imageListNormal:
                        image_w, image_h = theCtrl._imageListNormal.GetSize(self.GetImage())

                    if self.GetCheckedImage() is not None:
                        wcheck, hcheck = theCtrl._imageListCheck.GetSize(self.GetCheckedImage())

                    if wcheck and pointX <= self._x + wcheck + 1:
                        flags |= TREE_HITTEST_ONITEMCHECKICON
                        return self, flags

                    if image_w != -1 and pointX <= self._x + wcheck + image_w + 1:
                        flags |= TREE_HITTEST_ONITEMICON
                    else:
                        flags |= TREE_HITTEST_ONITEMLABEL

                    return self, flags

                if pointX < self._x:
                    if theCtrl.HasAGWFlag(TR_FULL_ROW_HIGHLIGHT):
                        flags |= TREE_HITTEST_ONITEM
                    else:
                        flags |= TREE_HITTEST_ONITEMINDENT
                if pointX > self._x + self._width:
                    if theCtrl.HasAGWFlag(TR_FULL_ROW_HIGHLIGHT):
                        flags |= TREE_HITTEST_ONITEM
                    else:
                        flags |= TREE_HITTEST_ONITEMRIGHT

                return self, flags

            # if children are expanded, fall through to evaluate them
            if not self.IsExpanded():
                return None, 0

        # evaluate children
        for child in self._children:
            res, flags = child.HitTest(point, theCtrl, flags, level + 1)
            if res is not None:
                return res, flags

        return None, 0


    def GetCurrentImage(self):
        """
        Returns the current item image.

        :return: An integer index that can be used to retrieve the item image inside
         a :class:`wx.ImageList`.
        """

        image = _NO_IMAGE

        if self.IsExpanded():

            if self.IsSelected():

                image = self._images[TreeItemIcon_SelectedExpanded]

            if image == _NO_IMAGE:

                # we usually fall back to the normal item, but try just the
                # expanded one (and not selected) first in this case
                image = self._images[TreeItemIcon_Expanded]

        else: # not expanded

            if self.IsSelected():
                image = self._images[TreeItemIcon_Selected]

        # maybe it doesn't have the specific image we want,
        # try the default one instead
        if image == _NO_IMAGE:
            image = self._images[TreeItemIcon_Normal]

        return image


    def GetCurrentCheckedImage(self):
        """
        Returns the current item check image.

        :return: An integer index that can be used to retrieve the item check image inside
         a :class:`wx.ImageList`.
        """

        if self._type == 0:
            return None

        checked = self.IsChecked()
        if checked:
            if self._type == 1:     # Checkbox
                if checked == wx.CHK_CHECKED:
                    return self._checkedimages[TreeItemIcon_Checked]
                else:
                    return self._checkedimages[TreeItemIcon_Undetermined]
            else:                   # Radiobutton
                return self._checkedimages[TreeItemIcon_Flagged]
        else:
            if self._type == 1:     # Checkbox
                return self._checkedimages[TreeItemIcon_NotChecked]
            else:                   # Radiobutton
                return self._checkedimages[TreeItemIcon_NotFlagged]


# -----------------------------------------------------------------------------
# CustomTreeCtrl Main Implementation.
# This Is The Main Class.
# -----------------------------------------------------------------------------

class CustomTreeCtrl(wx.ScrolledWindow):
    """
    :class:`CustomTreeCtrl` is a class that mimics the behaviour of :class:`TreeCtrl`, with almost the
    same base functionalities plus some more enhancements. This class does not rely on
    the native control, as it is a full owner-drawn tree control.
    """

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0, agwStyle=TR_DEFAULT_STYLE, validator=wx.DefaultValidator,
                 name="CustomTreeCtrl"):
        """
        Default class constructor.

        :param wx.Window `parent`: parent window. Must not be ``None``;
        :param integer `id`: window identifier. A value of -1 indicates a default value;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `pos`: tuple or :class:`wx.Point`
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :type `size`: tuple or :class:`wx.Size`
        :param integer `style`: the underlying :class:`ScrolledWindow` style;
        :param integer `agwStyle`: can be a combination of various bits. See
         :mod:`~wx.lib.agw.customtreectrl` for a full list of flags.
        :param wx.Validator `validator`: window validator;
        :param string `name`: window name.
        """

        self._current = self._key_current = self._anchor = self._select_me = None
        self._hasFocus = False
        self._dirty = False

        # Default line height: it will soon be changed
        self._lineHeight = 10
        # Item indent wrt parent
        self._indent = 15
        # item horizontal spacing between the start and the text
        self._spacing = 18

        # Brushes for focused/unfocused items (also gradient type)
        self._hilightBrush = wx.Brush(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        btnshadow = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNSHADOW)
        self._hilightUnfocusedBrush = wx.Brush(btnshadow)
        r, g, b = btnshadow.Red(), btnshadow.Green(), btnshadow.Blue()
        backcolour = (max((r >> 1) - 20, 0),
                      max((g >> 1) - 20, 0),
                      max((b >> 1) - 20, 0))
        backcolour = wx.Colour(backcolour[0], backcolour[1], backcolour[2])
        self._hilightUnfocusedBrush2 = wx.Brush(backcolour)

        # image list for icons
        self._imageListNormal = self._imageListButtons = self._imageListState = self._imageListCheck = self._imageListLeft = None
        self._ownsImageListNormal = self._ownsImageListButtons = self._ownsImageListState = self._ownsImageListLeft = False

        # Drag and drop initial settings
        self._dragCount = 0
        self._countDrag = 0
        self._isDragging = False
        self._dropTarget = self._oldSelection = None
        self._dragImage = None
        self._dragFullScreen = False
        self._underMouse = None

        # EditCtrl initial settings for editable items
        self._editCtrl = None
        self._editTimer = None

        # This one allows us to handle Freeze() and Thaw() calls
        self._freezeCount = 0

        self._findPrefix = ""
        self._findTimer = None

        self._dropEffectAboveItem = False
        self._lastOnSame = False

        # Default normal and bold fonts for an item
        self._hasFont = True
        self._normalFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        family = self._normalFont.GetFamily()
        if family == wx.FONTFAMILY_UNKNOWN:
            family = wx.FONTFAMILY_SWISS
        self._boldFont = wx.Font(self._normalFont.GetPointSize(), family,
                                 self._normalFont.GetStyle(), wx.FONTWEIGHT_BOLD, self._normalFont.GetUnderlined(),
                                 self._normalFont.GetFaceName(), self._normalFont.GetEncoding())
        self._italicFont = wx.Font(self._normalFont.GetPointSize(), family,
                                   wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, self._normalFont.GetUnderlined(),
                                   self._normalFont.GetFaceName(), self._normalFont.GetEncoding())

        # Hyperlinks things
        self._hypertextfont = wx.Font(self._normalFont.GetPointSize(), family,
                                      self._normalFont.GetStyle(), wx.FONTWEIGHT_NORMAL, True,
                                      self._normalFont.GetFaceName(), self._normalFont.GetEncoding())
        self._hypertextnewcolour = wx.BLUE
        self._hypertextvisitedcolour = wx.Colour(200, 47, 200)
        self._isonhyperlink = False

        # Default CustomTreeCtrl background colour.
        self._backgroundColour = wx.WHITE

        # Background image settings
        self._backgroundImage = None
        self._imageStretchStyle = _StyleTile

        # Disabled items colour
        self._disabledColour = wx.Colour(180, 180, 180)

        # Gradient selection colours
        self._firstcolour = colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self._secondcolour = wx.WHITE
        self._usegradients = False
        self._gradientstyle = 0   # Horizontal Gradient

        # Vista Selection Styles
        self._vistaselection = False

        # To speed up ExpandAll and SelectAll
        self._sendEvent = True

        # Connection lines style
        grey = (160,160,160)
        if wx.Platform != "__WXMAC__":
            self._dottedPen = wx.Pen(grey, 1, wx.USER_DASH)
            self._dottedPen.SetDashes([1,1])
            self._dottedPen.SetCap(wx.CAP_BUTT)
        else:
            self._dottedPen = wx.Pen(grey, 1)

        # Pen Used To Draw The Border Around Selected Items
        self._borderPen = wx.BLACK_PEN
        self._cursor = wx.Cursor(wx.CURSOR_ARROW)

        # For Appended Windows
        self._hasWindows = False
        self._itemWithWindow = []

        if wx.Platform == "__WXMAC__":
            agwStyle &= ~TR_LINES_AT_ROOT
            agwStyle |= TR_NO_LINES

            platform, major, minor, micro = wx.GetOsVersion()
            if major < 10:
                agwStyle |= TR_ROW_LINES

        # A constant to use my translation of RendererNative.DrawTreeItemButton
        # if the wxPython version is less than 2.6.2.1.
        if _VERSION_STRING < "2.6.2.1":
            self._drawingfunction = DrawTreeItemButton
        else:
            self._drawingfunction = wx.RendererNative.Get().DrawTreeItemButton

        # Set the separator pen default colour
        self._separatorPen = wx.Pen(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))

        # Create our container... at last!
        wx.ScrolledWindow.__init__(self, parent, id, pos, size, style|wx.HSCROLL|wx.VSCROLL, name)

        self._agwStyle = agwStyle

        # Create the default check image list
        self.SetImageListCheck(16, 16)

        # If the tree display has no buttons, but does have
        # connecting lines, we can use a narrower layout.
        # It may not be a good idea to force this...
        if not self.HasButtons() and not self.HasAGWFlag(TR_NO_LINES):
            self._indent= 10
            self._spacing = 10

        self.SetValidator(validator)

        attr = wx.ListCtrl.GetClassDefaultAttributes()
        self.SetOwnForegroundColour(attr.colFg)
        self.SetOwnBackgroundColour(attr.colBg)

        if not self._hasFont:
            self.SetOwnFont(attr.font)

        self.SetSize(size)

        # Bind the events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(EVT_TREE_ITEM_GETTOOLTIP, self.OnGetToolTip)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy, self)

        # Sets the focus to ourselves: this is useful if you have items
        # with associated widgets.
        self.SetFocus()


    def AcceptsFocus(self):
        """
        Can this window be given focus by mouse click?

        :note: This method always returns ``True`` as we always accept focus from
         mouse click.

        :note: Overridden from :class:`ScrolledWindow`.
        """

        # overridden base class method, allows this ctrl to
        # participate in the tab-order, etc.  It's overridable because
        # of deriving this class from wx.ScrolledWindow...
        return True


    def OnDestroy(self, event):
        """
        Handles the ``wx.EVT_WINDOW_DESTROY`` event for :class:`CustomTreeCtrl`.

        :param `event`: a :class:`wx.WindowDestroyEvent` event to be processed.
        """

        # Here there may be something I miss... do I have to destroy
        # something else?
        if self._editTimer and self._editTimer.IsRunning():
            self._editTimer.Stop()
            del self._editTimer
            self._editTimer = None

        if self._findTimer and self._findTimer.IsRunning():
            self._findTimer.Stop()
            del self._findTimer
            self._findTimer = None

        event.Skip()


    def GetControlBmp(self, checkbox=True, checked=False, enabled=True, x=16, y=16):
        """
        Returns a native looking checkbox or radio button bitmap.

        :param bool `checkbox`: ``True`` to get a checkbox image, ``False`` for a radiobutton one;
        :param bool `checked`: ``True`` if the control is marked, ``False`` if it is not;
        :param bool `enabled`: ``True`` if the control is enabled, ``False`` if it is not;
        :param integer `x`: the width of the bitmap;
        :param integer `y`: the height of the bitmap.

        :return: An instance of :class:`wx.Bitmap`, representing a native looking checkbox or radiobutton.
        """

        bmp = wx.Bitmap(x, y)
        mdc = wx.MemoryDC(bmp)
        mask = wx.Colour(0xfe, 0xfe, 0xfe)
        mdc.SetBackground(wx.Brush(mask))
        mdc.Clear()

        render = wx.RendererNative.Get()

        if checked == wx.CHK_CHECKED:
            flag = wx.CONTROL_CHECKED
        elif checked == wx.CHK_UNDETERMINED:
            flag = wx.CONTROL_UNDETERMINED
        else:
            flag = 0

        if not enabled:
            flag |= wx.CONTROL_DISABLED

        if checkbox:
            render.DrawCheckBox(self, mdc, (0, 0, x, y), flag)
        else:
            if _VERSION_STRING < "2.9":
                render.DrawRadioButton(self, mdc, (0, 0, x, y), flag)
            else:
                render.DrawRadioBitmap(self, mdc, (0, 0, x, y), flag)

        mdc.SelectObject(wx.NullBitmap)
        bmp.SetMaskColour(mask)
        return bmp


    def GetCount(self):
        """ Returns the global number of items in the tree. """

        if not self._anchor:
            # the tree is empty
            return 0

        count = self._anchor.GetChildrenCount()

        if not self.HasAGWFlag(TR_HIDE_ROOT):
            # take the root itself into account
            count = count + 1

        return count


    def GetIndent(self):
        """ Returns the item indentation, in pixels. """

        return self._indent


    def GetSpacing(self):
        """ Returns the spacing between the start and the text, in pixels. """

        return self._spacing


    def GetRootItem(self):
        """ Returns the root item, an instance of :class:`GenericTreeItem`. """

        return self._anchor


    def GetSelection(self):
        """
        Returns the current selected item (i.e. focused item).

        :return: An instance of :class:`GenericTreeItem`.

        :note: Similar to GetFocusedItem of wx.TreeCtrl. Use
         :meth:`~CustomTreeCtrl.GetSelections` for obtaining all items
         selected in multiple-selection trees (i.e. TR_MULTIPLE flag set).
        """

        return self._current

    GetFocusedItem = GetSelection


    def ToggleItemSelection(self, item):
        """
        Toggles the item selection.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        self.SelectItem(item, not self.IsSelected(item))


    def EnableChildren(self, item, enable=True):
        """
        Enables/disables the item children.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `enable`: ``True`` to enable the children, ``False`` to disable them.

        :note: This method is used internally.
        """

        torefresh = False
        if item.IsExpanded():
            torefresh = True

        if item.GetType() == 2 and enable and not item.IsChecked():
            # We hit a radiobutton item not checked, we don't want to
            # enable the children
            return

        child, cookie = self.GetFirstChild(item)
        while child:
            self.EnableItem(child, enable, torefresh=torefresh)
            # Recurse on tree
            if child.GetType != 2 or (child.GetType() == 2 and item.IsChecked()):
                self.EnableChildren(child, enable)
            (child, cookie) = self.GetNextChild(item, cookie)


    def EnableItem(self, item, enable=True, torefresh=True):
        """
        Enables/disables an item.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `enable`: ``True`` to enable the item, ``False`` to disable it;
        :param bool `torefresh`: whether to redraw the item or not.
        """

        if item.IsEnabled() == enable:
            return

        if not enable and item.IsSelected():
            self.SelectItem(item, False)

        item.Enable(enable)
        wnd = item.GetWindow()

        # Handles the eventual window associated to the item
        if wnd:
            wndenable = item.GetWindowEnabled()
            wnd.Enable(enable)

        if torefresh:
            # We have to refresh the item line
            dc = wx.ClientDC(self)
            self.CalculateSize(item, dc)
            self.RefreshLine(item)


    def IsItemEnabled(self, item):
        """
        Returns whether an item is enabled or disabled.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        return item.IsEnabled()


    def SetDisabledColour(self, colour):
        """
        Sets the colour for items in a disabled state.

        :param `colour`: a valid :class:`wx.Colour` instance.
        """

        self._disabledColour = colour
        self._dirty = True


    def GetDisabledColour(self):
        """
        Returns the colour for items in a disabled state.

        :return: An instance of :class:`wx.Colour`.
        """

        return self._disabledColour


    def IsItemChecked(self, item):
        """
        Returns whether an item is checked or not.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: ``True`` if the item is in a 'checked' state, ``False`` otherwise.

        :note: This method is meaningful only for checkbox-like and radiobutton-like items.
        """

        return item.IsChecked()


    def GetItem3StateValue(self, item):
        """
        Gets the state of a 3-state checkbox item.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: ``wx.CHK_UNCHECKED`` when the checkbox is unchecked, ``wx.CHK_CHECKED``
         when it is checked and ``wx.CHK_UNDETERMINED`` when it's in the undetermined
         state.

        :note: This method raises an exception when the function is used with a 2-state
         checkbox item.

        :note: This method is meaningful only for checkbox-like items.
        """

        return item.Get3StateValue()


    def IsItem3State(self, item):
        """
        Returns whether or not the checkbox item is a 3-state checkbox.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: ``True`` if this checkbox is a 3-state checkbox, ``False`` if it's a
         2-state checkbox item.

        :note: This method is meaningful only for checkbox-like items.
        """

        return item.Is3State()


    def SetItem3StateValue(self, item, state):
        """
        Sets the checkbox item to the given `state`.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param integer `state`: can be one of: ``wx.CHK_UNCHECKED`` (check is off), ``wx.CHK_CHECKED``
         (check is on) or ``wx.CHK_UNDETERMINED`` (check is mixed).

        :note: This method raises an exception when the checkbox item is a 2-state checkbox
         and setting the state to ``wx.CHK_UNDETERMINED``.

        :note: This method is meaningful only for checkbox-like items.
        """

        item.Set3StateValue(state)


    def SetItem3State(self, item, allow):
        """
        Sets whether the item has a 3-state value checkbox assigned to it or not.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `allow`: ``True`` to set an item as a 3-state checkbox, ``False`` to set it
         to a 2-state checkbox.

        :return: ``True`` if the change was successful, ``False`` otherwise.

        :note: This method is meaningful only for checkbox-like items.
        """

        return item.Set3State(allow)


    def CheckItem2(self, item, checked=True, torefresh=False):
        """
        Used internally to avoid ``EVT_TREE_ITEM_CHECKED`` events.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `checked`: ``True`` to check an item, ``False`` to uncheck it;
        :param bool `torefresh`: whether to redraw the item or not.
        """

        if item.GetType() == 0:
            return

        item.Check(checked)

        if torefresh:
            dc = wx.ClientDC(self)
            self.CalculateSize(item, dc)
            self.RefreshLine(item)


    def UnCheckRadioParent(self, item, checked=False):
        """
        Used internally to handle radio node parent correctly.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `checked`: ``True`` to check an item, ``False`` to uncheck it.
        """

        e = TreeEvent(wxEVT_TREE_ITEM_CHECKING, self.GetId())
        e.SetItem(item)
        e.SetEventObject(self)

        if self.GetEventHandler().ProcessEvent(e):
            return False

        item.Check(checked)
        self.RefreshLine(item)
        self.EnableChildren(item, checked)
        e = TreeEvent(wxEVT_TREE_ITEM_CHECKED, self.GetId())
        e.SetItem(item)
        e.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(e)

        return True


    def CheckItem(self, item, checked=True):
        """
        Actually checks/uncheks an item, sending (eventually) the two
        events ``EVT_TREE_ITEM_CHECKING`` and ``EVT_TREE_ITEM_CHECKED``.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `checked`: for a radiobutton-type item, ``True`` to check it, ``False``
         to uncheck it. For a checkbox-type item, it can be one of ``wx.CHK_UNCHECKED``
         when the checkbox is unchecked, ``wx.CHK_CHECKED`` when it is checked and
         ``wx.CHK_UNDETERMINED`` when it's in the undetermined state.
        """

        # Should we raise an error here?!?
        if item.GetType() == 0:
            return

        if item.GetType() == 2:    # it's a radio button
            if not checked and item.IsChecked():  # Try To Unckeck?
                return
            else:
                if not self.UnCheckRadioParent(item, checked):
                    return

                self.CheckSameLevel(item, False)
                return

        # Radiobuttons are done, let's handle checkbuttons...
        e = TreeEvent(wxEVT_TREE_ITEM_CHECKING, self.GetId())
        e.SetItem(item)
        e.SetEventObject(self)

        if self.GetEventHandler().ProcessEvent(e):
            # Blocked by user
            return

        if item.Is3State():
            item.Set3StateValue(checked)
        else:
            item.Check(checked)

        dc = wx.ClientDC(self)
        self.RefreshLine(item)

        if self.HasAGWFlag(TR_AUTO_CHECK_CHILD):
            ischeck = self.IsItemChecked(item)
            self.AutoCheckChild(item, ischeck)
        if self.HasAGWFlag(TR_AUTO_CHECK_PARENT):
            ischeck = self.IsItemChecked(item)
            self.AutoCheckParent(item, ischeck)
        elif self.HasAGWFlag(TR_AUTO_TOGGLE_CHILD):
            self.AutoToggleChild(item)

        e = TreeEvent(wxEVT_TREE_ITEM_CHECKED, self.GetId())
        e.SetItem(item)
        e.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(e)


    def AutoToggleChild(self, item):
        """
        Transverses the tree and toggles the items.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :note: This method is meaningful only for checkbox-like and radiobutton-like items.
        """

        child, cookie = self.GetFirstChild(item)

        torefresh = False
        if item.IsExpanded():
            torefresh = True

        # Recurse on tree
        while child:
            if child.GetType() == 1 and child.IsEnabled():
                self.CheckItem2(child, not child.IsChecked(), torefresh=torefresh)
            self.AutoToggleChild(child)
            (child, cookie) = self.GetNextChild(item, cookie)


    def AutoCheckChild(self, item, checked):
        """
        Transverses the tree and checks/unchecks the items.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `checked`: ``True`` to check an item, ``False`` to uncheck it.

        :note: This method is meaningful only for checkbox-like and radiobutton-like items.
        """

        (child, cookie) = self.GetFirstChild(item)

        torefresh = False
        if item.IsExpanded():
            torefresh = True

        while child:
            if child.GetType() == 1 and child.IsEnabled():
                self.CheckItem2(child, checked, torefresh=torefresh)
            self.AutoCheckChild(child, checked)
            (child, cookie) = self.GetNextChild(item, cookie)


    def AutoCheckParent(self, item, checked):
        """
        Traverses up the tree and checks/unchecks parent items.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `checked`: ``True`` to check an item, ``False`` to uncheck it.

        :note: This method is meaningful only for checkbox-like and radiobutton-like items.
        """

        parent = item.GetParent()
        if not parent or parent.GetType() != 1:
            return

        (child, cookie) = self.GetFirstChild(parent)
        while child:
            if child.GetType() == 1 and child.IsEnabled():
                if checked != child.IsChecked():
                    return
            (child, cookie) = self.GetNextChild(parent, cookie)

        self.CheckItem2(parent, checked, torefresh=True)
        self.AutoCheckParent(parent, checked)


    def CheckChilds(self, item, checked=True):
        """
        Programmatically check/uncheck item children.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `checked`: ``True`` to check an item, ``False`` to uncheck it.

        :note: This method is meaningful only for checkbox-like and radiobutton-like items.

        :note: This method does not generate ``EVT_TREE_ITEM_CHECKING`` and
         ``EVT_TREE_ITEM_CHECKED`` events.
        """

        if checked is None:
            self.AutoToggleChild(item)
        else:
            self.AutoCheckChild(item, checked)


    def CheckSameLevel(self, item, checked=False):
        """
        Uncheck radio items which are on the same level of the checked one.
        Used internally.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `checked`: ``True`` to check an item, ``False`` to uncheck it.

        :note: This method is meaningful only for radiobutton-like items.
        """

        parent = item.GetParent()

        if not parent:
            return

        torefresh = False
        if parent.IsExpanded():
            torefresh = True

        (child, cookie) = self.GetFirstChild(parent)
        while child:
            if child.GetType() == 2 and child != item:
                self.CheckItem2(child, checked, torefresh=torefresh)
                if child.GetType != 2 or (child.GetType() == 2 and child.IsChecked()):
                    self.EnableChildren(child, checked)
            (child, cookie) = self.GetNextChild(parent, cookie)


    def EditLabel(self, item):
        """
        Starts editing an item label.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        self.Edit(item)


    def ShouldInheritColours(self):
        """
        Return ``True`` from here to allow the colours of this window to be
        changed by `InheritAttributes`, returning ``False`` forbids inheriting them
        from the parent window.

        The base class version returns ``False``, but this method is overridden in
        :class:`wx.Control` where it returns ``True``.

        :class:`CustomTreeCtrl` does not inherit colours from anyone.
        """

        return False


    def SetIndent(self, indent):
        """
        Sets the indentation for :class:`CustomTreeCtrl`.

        :param integer `indent`: an integer representing the indentation for the items in the tree.
        """

        self._indent = indent
        self._dirty = True


    def SetSpacing(self, spacing):
        """
        Sets the spacing between items in :class:`CustomTreeCtrl`.

        :param integer `spacing`: an integer representing the spacing between items in the tree.
        """

        self._spacing = spacing
        self._dirty = True


    def HasChildren(self, item):
        """
        Returns whether an item has children or not.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        return len(item.GetChildren()) > 0


    def GetChildrenCount(self, item, recursively=True):
        """
        Returns the item children count.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `recursively`: if ``True``, returns the total number of descendants,
         otherwise only one level of children is counted.
        """

        return item.GetChildrenCount(recursively)


    def HasAGWFlag(self, flag):
        """
        Returns ``True`` if :class:`CustomTreeCtrl` has the `flag` bit set.

        :param integer `flag`: any possible window style for :class:`CustomTreeCtrl`.

        :see: The :meth:`~CustomTreeCtrl.__init__` method for the `flag` parameter description.
        """

        return bool(self._agwStyle & flag)


    def SetAGWWindowStyleFlag(self, agwStyle):
        """
        Sets the :class:`CustomTreeCtrl` window style.

        :param integer `agwStyle`: the new :class:`CustomTreeCtrl` window style.

        :see: The :meth:`~CustomTreeCtrl.__init__` method for the `agwStyle` parameter description.
        """

        # Do not try to expand the root node if it hasn't been created yet
        if self._anchor and not self.HasAGWFlag(TR_HIDE_ROOT) and agwStyle & TR_HIDE_ROOT:

            # if we will hide the root, make sure children are visible
            self._anchor.SetHasPlus()
            self._anchor.Expand()
            self.CalculatePositions()

        # right now, just sets the styles.  Eventually, we may
        # want to update the inherited styles, but right now
        # none of the parents has updatable styles

        if self.HasAGWFlag(TR_MULTIPLE) and not (agwStyle & TR_MULTIPLE):
            selections = self.GetSelections()
            for select in selections[0:-1]:
                self.SelectItem(select, False)

        self._agwStyle = agwStyle
        self._dirty = True


    def GetAGWWindowStyleFlag(self):
        """
        Returns the :class:`CustomTreeCtrl` style.

        :see: The :meth:`~CustomTreeCtrl.__init__` method for a list of possible style flags.
        """

        return self._agwStyle


    def HasButtons(self):
        """
        Returns whether :class:`CustomTreeCtrl` has the ``TR_HAS_BUTTONS`` flag set.

        :return: ``True`` if :class:`CustomTreeCtrl` has the ``TR_HAS_BUTTONS`` flag set,
         ``False`` otherwise.
        """

        return self.HasAGWFlag(TR_HAS_BUTTONS)


# -----------------------------------------------------------------------------
# functions to work with tree items
# -----------------------------------------------------------------------------

    def GetItemText(self, item):
        """
        Returns the item text.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        return item.GetText()


    def GetItemSize(self, item):
        """
        Returns the horizontal space available in :class:`CustomTreeCtrl`, in pixels, to draw this item.

        :param `item`: an instance of :class:`GenericTreeItem`.

        .. versionadded:: 0.9.3
        """

        w, h = self.GetClientSize()
        xa, ya = self.CalcScrolledPosition((0, item.GetY()))

        wcheck = image_w = 0

        if item.GetType() != 0:
            wcheck, dummy = self._imageListCheck.GetSize(item.GetType())
            wcheck += 4

        image = item.GetCurrentImage()

        if image != _NO_IMAGE:
            if self._imageListNormal:
                image_w, dummy = self._imageListNormal.GetSize(image)
                image_w += 4

        maxsize = w - (wcheck + image_w + item.GetX()) + xa
        return maxsize


    def GetItemImage(self, item, which=TreeItemIcon_Normal):
        """
        Returns the item image.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param integer `which`: can be one of the following bits:

         ================================= ========================
         Item State                        Description
         ================================= ========================
         ``TreeItemIcon_Normal``           To get the normal item image
         ``TreeItemIcon_Selected``         To get the selected item image (i.e. the image which is shown when the item is currently selected)
         ``TreeItemIcon_Expanded``         To get the expanded image (this only makes sense for items which have children - then this image is shown when the item is expanded and the normal image is shown when it is collapsed)
         ``TreeItemIcon_SelectedExpanded`` To get the selected expanded image (which is shown when an expanded item is currently selected)
         ================================= ========================

        :return: An integer index that can be used to retrieve the item image inside
         a :class:`wx.ImageList`.
        """

        return item.GetImage(which)


    def GetItemLeftImage(self, item):
        """
        Returns the item leftmost image, i.e. the image associated to the item on the leftmost
        part of the :class:`CustomTreeCtrl` client area.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: An integer index that can be used to retrieve the item leftmost image inside
         a :class:`wx.ImageList`.
        """

        return item.GetLeftImage()


    def GetPyData(self, item):
        """
        Returns the data associated to an item.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: A Python object representing the item data, or ``None`` if no data
         has been assigned to this item.
        """

        return item.GetData()

    GetItemPyData = GetPyData
    GetItemData   = GetPyData


    def GetItemTextColour(self, item):
        """
        Returns the item text colour or separator horizontal line colour.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: An instance of :class:`wx.Colour`.
        """

        return item.Attr().GetTextColour()


    def GetItemBackgroundColour(self, item):
        """
        Returns the item background colour.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: An instance of :class:`wx.Colour`.
        """

        return item.Attr().GetBackgroundColour()


    def GetItemFont(self, item):
        """
        Returns the item font.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: An instance of :class:`wx.Font`.
        """

        font = item.Attr().GetFont()
        if font.IsOk():
            return font

        return wx.NullFont


    def IsItemHyperText(self, item):
        """
        Returns whether an item is hypertext or not.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: ``True`` if the item is hypertext-like, ``False`` otherwise.
        """

        return item.IsHyperText()


    def SetItemText(self, item, text):
        """
        Sets the item text.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param string `text`: the new item label.

        :raise: `Exception` if the input `item` is a separator.
        """

        if item.IsSeparator():
            raise Exception("Separator items can not have text")

        dc = wx.ClientDC(self)
        oldtext = item.GetText()
        item.SetText(text)
        # Avoid Calculating tree unless number of lines changed (slow).
        if oldtext.count('\n') != text.count('\n'):
            self.CalculatePositions()
            self.Refresh()
            self.AdjustMyScrollbars()
        else:
            self.CalculateSize(item, dc)
            self.RefreshLine(item)


    def SetItemImage(self, item, image, which=TreeItemIcon_Normal):
        """
        Sets the item image, depending on the item state.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param integer `image`: an index within the normal image list specifying the image to
         use for the item in the state specified by the `which` parameter;
        :param integer `which`: the item state.

        :see: :meth:`~CustomTreeCtrl.GetItemImage` for an explanation of the `which` parameter.
        """

        item.SetImage(image, which)

        dc = wx.ClientDC(self)
        self.CalculateSize(item, dc)
        self.RefreshLine(item)


    def SetItemLeftImage(self, item, image):
        """
        Sets the item leftmost image, i.e. the image associated to the item on the leftmost
        part of the :class:`CustomTreeCtrl` client area.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param integer `image`: an index within the left image list specifying the image to
         use for the item in the leftmost part of the client area.
        """

        item.SetLeftImage(image)

        dc = wx.ClientDC(self)
        self.CalculateSize(item, dc)
        self.RefreshLine(item)


    def SetPyData(self, item, data):
        """
        Sets the data associated to an item.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param object `data`: can be any Python object.
        """

        item.SetData(data)

    SetItemPyData = SetPyData
    SetItemData = SetPyData


    def SetItemHasChildren(self, item, has=True):
        """
        Forces the appearance/disappearance of the button next to the item.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `has`: ``True`` to have a button next to an item, ``False`` otherwise.
        """

        item.SetHasPlus(has)
        self.RefreshLine(item)


    def SetItemBold(self, item, bold=True):
        """
        Sets the item font as bold/unbold.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `bold`: ``True`` to set the item font as bold, ``False`` otherwise.
        """

        # avoid redrawing the tree if no real change
        if item.IsBold() != bold:
            item.SetBold(bold)
            self._dirty = True


    def SetItemItalic(self, item, italic=True):
        """
        Sets the item font as italic/non-italic.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `italic`: ``True`` to set the item font as italic, ``False`` otherwise.
        """

        if item.IsItalic() != italic:
            item.SetItalic(italic)
            self._dirty = True


    def SetItemDropHighlight(self, item, highlight=True):
        """
        Gives the item the visual feedback for drag and drop operations.
        This is useful when something is dragged from outside the :class:`CustomTreeCtrl`.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `highlight`: ``True`` to highlight the dragged items, ``False`` otherwise.
        """

        if highlight:
            bg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
            fg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)

        item.Attr().SetTextColour(fg)
        item.Attr.SetBackgroundColour(bg)
        self.RefreshLine(item)


    def SetItemTextColour(self, item, colour):
        """
        Sets the item text colour or separator horizontal line colour.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param `colour`: a valid :class:`wx.Colour` instance.
        """

        item.Attr().SetTextColour(colour)
        self.RefreshLine(item)


    def SetItemBackgroundColour(self, item, colour):
        """
        Sets the item background colour.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param `colour`: a valid :class:`wx.Colour` instance.
        """

        item.Attr().SetBackgroundColour(colour)
        self.RefreshLine(item)


    def SetItemHyperText(self, item, hyper=True):
        """
        Sets whether the item is hypertext or not.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `hyper`: ``True`` to have an item with hypertext behaviour, ``False`` otherwise.
        """

        item.SetHyperText(hyper)
        self.RefreshLine(item)


    def SetItemFont(self, item, font):
        """
        Sets the item font.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param `font`: a valid :class:`wx.Font` instance.
        """

        item.Attr().SetFont(font)
        self._dirty = True


    def SetFont(self, font):
        """
        Sets the :class:`CustomTreeCtrl` font.

        :param `font`: a valid :class:`wx.Font` instance.

        :note: Overridden from :class:`ScrolledWindow`.
        """

        wx.ScrolledWindow.SetFont(self, font)

        self._normalFont = font
        family = self._normalFont.GetFamily()

        if family == wx.FONTFAMILY_UNKNOWN:
            family = wx.FONTFAMILY_SWISS

        self._boldFont = wx.Font(self._normalFont.GetPointSize(), family,
                                 self._normalFont.GetStyle(), wx.FONTWEIGHT_BOLD, self._normalFont.GetUnderlined(),
                                 self._normalFont.GetFaceName(), self._normalFont.GetEncoding())

        self._italicFont = wx.Font(self._normalFont.GetPointSize(), family,
                                   wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, self._normalFont.GetUnderlined(),
                                   self._normalFont.GetFaceName(), self._normalFont.GetEncoding())

        self.CalculatePositions()
        self.Refresh()
        self.AdjustMyScrollbars()

        return True


    def GetHyperTextFont(self):
        """
        Returns the font used to render hypertext items.

        :return: An instance of :class:`wx.Font`.

        :note: This method is meaningful only for hypertext-like items.
        """

        return self._hypertextfont


    def SetHyperTextFont(self, font):
        """
        Sets the font used to render hypertext items.

        :param `font`: a valid :class:`wx.Font` instance.

        :note: This method is meaningful only for hypertext-like items.
        """

        self._hypertextfont = font
        self._dirty = True


    def SetHyperTextNewColour(self, colour):
        """
        Sets the colour used to render a non-visited hypertext item.

        :param `colour`: a valid :class:`wx.Colour` instance.

        :note: This method is meaningful only for hypertext-like items.
        """

        self._hypertextnewcolour = colour
        self._dirty = True


    def GetHyperTextNewColour(self):
        """
        Returns the colour used to render a non-visited hypertext item.

        :return: An instance of :class:`wx.Colour`.

        :note: This method is meaningful only for hypertext-like items.
        """

        return self._hypertextnewcolour


    def SetHyperTextVisitedColour(self, colour):
        """
        Sets the colour used to render a visited hypertext item.

        :param `colour`: a valid :class:`wx.Colour` instance.

        :note: This method is meaningful only for hypertext-like items.
        """

        self._hypertextvisitedcolour = colour
        self._dirty = True


    def GetHyperTextVisitedColour(self):
        """
        Returns the colour used to render a visited hypertext item.

        :return: An instance of :class:`wx.Colour`.

        :note: This method is meaningful only for hypertext-like items.
        """

        return self._hypertextvisitedcolour


    def SetItemVisited(self, item, visited=True):
        """
        Sets whether an hypertext item was visited.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `visited`: ``True`` to mark an hypertext item as visited, ``False`` otherwise.

        :note: This method is meaningful only for hypertext-like items.
        """

        item.SetVisited(visited)
        self.RefreshLine(item)


    def GetItemVisited(self, item):
        """
        Returns whether an hypertext item was visited.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: ``True`` if the hypertext item has been visited, ``False`` otherwise.

        :note: This method is meaningful only for hypertext-like items.
        """

        return item.GetVisited()


    def SetHilightFocusColour(self, colour):
        """
        Sets the colour used to highlight focused selected items.

        :param `colour`: a valid :class:`wx.Colour` instance.

        :note: This is applied only if gradient and Windows Vista selection
         styles are disabled.
        """

        self._hilightBrush = wx.Brush(colour)
        self.RefreshSelected()


    def SetHilightNonFocusColour(self, colour):
        """
        Sets the colour used to highlight unfocused selected items.

        :param `colour`: a valid :class:`wx.Colour` instance.

        :note: This is applied only if gradient and Windows Vista selection
         styles are disabled.
        """

        self._hilightUnfocusedBrush = wx.Brush(colour)
        self.RefreshSelected()


    def GetHilightFocusColour(self):
        """
        Returns the colour used to highlight focused selected items.

        :return: An instance of :class:`wx.Colour`.

        :note: This is used only if gradient and Windows Vista selection
         styles are disabled.
        """

        return self._hilightBrush.GetColour()


    def GetHilightNonFocusColour(self):
        """
        Returns the colour used to highlight unfocused selected items.

        :return: An instance of :class:`wx.Colour`.

        :note: This is used only if gradient and Windows Vista selection
         styles are disabled.
        """

        return self._hilightUnfocusedBrush.GetColour()


    def SetFirstGradientColour(self, colour=None):
        """
        Sets the first gradient colour for gradient-style selections.

        :param `colour`: if not ``None``, a valid :class:`wx.Colour` instance. Otherwise,
         the colour is taken from the system value ``wx.SYS_COLOUR_HIGHLIGHT``.
        """

        if colour is None:
            colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)

        self._firstcolour = colour
        if self._usegradients:
            self.RefreshSelected()


    def SetSecondGradientColour(self, colour=None):
        """
        Sets the second gradient colour for gradient-style selections.

        :param `colour`: if not ``None``, a valid :class:`wx.Colour` instance. Otherwise,
         the colour generated is a slightly darker version of the :class:`CustomTreeCtrl`
         background colour.
        """

        if colour is None:
            # No colour given, generate a slightly darker from the
            # CustomTreeCtrl background colour
            colour = self.GetBackgroundColour()
            r, g, b = int(colour.Red()), int(colour.Green()), int(colour.Blue())
            colour = ((r >> 1) + 20, (g >> 1) + 20, (b >> 1) + 20)
            colour = wx.Colour(colour[0], colour[1], colour[2])

        self._secondcolour = colour

        if self._usegradients:
            self.RefreshSelected()


    def GetFirstGradientColour(self):
        """
        Returns the first gradient colour for gradient-style selections.

        :return: An instance of :class:`wx.Colour`.
        """

        return self._firstcolour


    def GetSecondGradientColour(self):
        """
        Returns the second gradient colour for gradient-style selections.

        :return: An instance of :class:`wx.Colour`.
        """

        return self._secondcolour


    def EnableSelectionGradient(self, enable=True):
        """
        Globally enables/disables drawing of gradient selections.

        :param bool `enable`: ``True`` to enable gradient-style selections, ``False``
         to disable it.

        :note: Calling this method disables any Vista-style selection previously
         enabled.
        """

        self._usegradients = enable
        self._vistaselection = False
        self.RefreshSelected()


    def SetGradientStyle(self, vertical=0):
        """
        Sets the gradient style for gradient-style selections.

        :param integer `vertical`: ``0`` for horizontal gradient-style selections, ``1`` for vertical
         gradient-style selections.
        """

        # 0 = Horizontal, 1 = Vertical
        self._gradientstyle = vertical

        if self._usegradients:
            self.RefreshSelected()


    def GetGradientStyle(self):
        """
        Returns the gradient style for gradient-style selections.

        :return: ``0`` for horizontal gradient-style selections, ``1`` for vertical
         gradient-style selections.
        """

        return self._gradientstyle


    def EnableSelectionVista(self, enable=True):
        """
        Globally enables/disables drawing of Windows Vista selections.

        :param bool `enable`: ``True`` to enable Vista-style selections, ``False`` to
         disable it.

        :note: Calling this method disables any gradient-style selection previously
         enabled.
        """

        self._usegradients = False
        self._vistaselection = enable
        self.RefreshSelected()


    def SetBorderPen(self, pen):
        """
        Sets the pen used to draw the selected item border.

        :param `pen`: an instance of :class:`wx.Pen`.

        :note: The border pen is not used if the Windows Vista selection style is applied.
        """

        self._borderPen = pen
        self.RefreshSelected()


    def GetBorderPen(self):
        """
        Returns the pen used to draw the selected item border.

        :return: An instance of :class:`wx.Pen`.

        :note: The border pen is not used if the Windows Vista selection style is applied.
        """

        return self._borderPen


    def SetConnectionPen(self, pen):
        """
        Sets the pen used to draw the connecting lines between items.

        :param `pen`: an instance of :class:`wx.Pen`.
        """

        self._dottedPen = pen
        self._dirty = True


    def GetConnectionPen(self):
        """
        Returns the pen used to draw the connecting lines between items.

        :return: An instance of :class:`wx.Pen`.
        """

        return self._dottedPen


    def SetBackgroundImage(self, image):
        """
        Sets the :class:`CustomTreeCtrl` background image.

        :param `image`: if not ``None``, an instance of :class:`wx.Bitmap`.

        :note: At present, the background image can only be used in "tile" mode.

        .. todo:: Support background images also in stretch and centered modes.
        """

        self._backgroundImage = image
        self.Refresh()


    def GetBackgroundImage(self):
        """
        Returns the :class:`CustomTreeCtrl` background image (if any).

        :return: An instance of :class:`wx.Bitmap` if a background image is present, ``None`` otherwise.

        :note: At present, the background image can only be used in "tile" mode.

        .. todo:: Support background images also in stretch and centered modes.
        """

        return self._backgroundImage


    def SetSeparatorColour(self, colour):
        """
        Sets the pen colour for separator-type items.

        :param `colour`: a valid instance of :class:`wx.Colour`.
        """

        self._separatorPen = wx.Pen(colour, 1)
        self.Refresh()


    def GetSeparatorColour(self, colour):
        """
        Returns the pen colour for separator-type items.

        :return: An instance of :class:`wx.Colour` representing the separator pen colour.
        """

        return self._separatorPen.GetColour()


    def IsItemSeparator(self, item):
        """
        Returns whether an item is of separator type or not.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        return item.IsSeparator()


    def GetItemWindow(self, item):
        """
        Returns the window associated to the item (if any).

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: An instance of :class:`wx.Window` if the item has an associated window, ``None`` otherwise.
        """

        return item.GetWindow()


    def SetItemWindow(self, item, wnd, on_the_right=True):
        """
        Sets the window for the given item.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param `wnd`: if not ``None``, a non-toplevel window to be displayed next to
         the item.
        :param bool `on_the_right`: ``True`` positions the window on the right of text, ``False``
         on the left of text and overlapping the image. New in wxPython 4.0.4.

        :raise: `Exception` if the input `item` is a separator and `wnd` is not ``None``.
        """

        if item.IsSeparator() and wnd is not None:
            raise Exception("Separator items can not have an associated window")

        if wnd is not None:
            self._hasWindows = True
            if item not in self._itemWithWindow:
                self._itemWithWindow.append(item)
            else:
                self.DeleteItemWindow(item)
        else:
            self.DeleteItemWindow(item)

        item.SetWindow(wnd, on_the_right)
        self.CalculatePositions()
        self.Refresh()
        self.AdjustMyScrollbars()


    def DeleteItemWindow(self, item):
        """
        Deletes the window associated to an item (if any).

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        if item.GetWindow() is None:
            return

        item.DeleteWindow()
        if item in self._itemWithWindow:
            self._itemWithWindow.remove(item)
        self._dirty = True


    def GetItemWindowEnabled(self, item):
        """
        Returns whether the window associated to the item is enabled.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: ``True`` if the item has an associated window and this window is
         enabled, ``False`` in all other cases.
        """

        return item.GetWindowEnabled()


    def SetItemWindowEnabled(self, item, enable=True):
        """
        Enables/disables the window associated to the item.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `enable`: ``True`` to enable the associated window, ``False`` to
         disable it.
        """

        item.SetWindowEnabled(enable)


    def GetItemType(self, item):
        """
        Returns the item type.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: An integer representing the item type.

        :see: :meth:`~CustomTreeCtrl.SetItemType` for a description of valid item types.
        """

        return item.GetType()


    def SetItemType(self, item, ct_type):
        """
        Sets the item type.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param integer `ct_type`: may be one of the following integers:

         =============== =========================================
         `ct_type` Value Description
         =============== =========================================
                0        A normal item
                1        A checkbox-like item
                2        A radiobutton-type item
         =============== =========================================

        :note: Regarding radiobutton-type items (with `ct_type` = 2), the following
         approach is used:

         - All peer-nodes that are radiobuttons will be mutually exclusive. In other words,
           only one of a set of radiobuttons that share a common parent can be checked at
           once. If a radiobutton node becomes checked, then all of its peer radiobuttons
           must be unchecked.
         - If a radiobutton node becomes unchecked, then all of its child nodes will become
           inactive.

        """

        item.SetType(ct_type)
        self.CalculatePositions()
        self.Refresh()


    def GetDragFullScreen(self):
        """
        Returns whether built-in drag/drop will be full screen or not.

        :return: ``True`` if the drag/drop operation will be full screen, or
         ``False`` if only within the tree.
        """

        return self._dragFullScreen


    def SetDragFullScreen(self, fullScreen=False):
        """
        Sets whether a drag operation will be performed full screen or not.

        A full screen drag allows the user to drag outside of the tree to
        other controls. When the drag is finished the destination will have
        to be found manually in the ``EVT_TREE_END_DRAG`` handler with
        something like:

        example::

            wnd = wx.FindWindowAtPoint(self.ClientToScreen(event.GetPoint()))

        :param bool `fullScreen`: False (default) to drag within tree only.
        """

        self._dragFullScreen = bool(fullScreen)


# -----------------------------------------------------------------------------
# item status inquiries
# -----------------------------------------------------------------------------

    def IsVisible(self, item):
        """
        Returns whether the item is visible or not (i.e., its hierarchy is expanded
        enough to show the item, and it has not been hidden).

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: ``True`` if the item is visible, ``False`` if it is hidden.
        """
        # Hidden items are never visible.
        if item.IsHidden():
            return False
        
        # An item is only visible if it's not a descendant of a collapsed item
        parent = item.GetParent()

        while parent:

            if not parent.IsExpanded():
                return False

            parent = parent.GetParent()

        startX, startY = self.GetViewStart()
        clientSize = self.GetClientSize()

        rect = self.GetBoundingRect(item)

        if not rect:
            return False
        if rect.GetWidth() == 0 or rect.GetHeight() == 0:
            return False
        if rect.GetBottom() < 0 or rect.GetTop() > clientSize.y:
            return False
        if rect.GetRight() < 0 or rect.GetLeft() > clientSize.x:
            return False

        return True


    def ItemHasChildren(self, item):
        """
        Returns whether the item has children or not.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: ``True`` if the item has children, ``False`` otherwise.
        """

        # consider that the item does have children if it has the "+" button: it
        # might not have them (if it had never been expanded yet) but then it
        # could have them as well and it's better to err on this side rather than
        # disabling some operations which are restricted to the items with
        # children for an item which does have them
        return item.HasPlus()


    def IsExpanded(self, item):
        """
        Returns whether the item is expanded or not.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: ``True`` if the item is expanded, ``False`` if it is collapsed.
        """

        return item.IsExpanded()


    def IsSelected(self, item):
        """
        Returns whether the item is selected or not.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: ``True`` if the item is selected, ``False`` otherwise.
        """

        return item.IsSelected()


    def IsBold(self, item):
        """
        Returns whether the item font is bold or not.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: ``True`` if the item has bold text, ``False`` otherwise.
        """

        return item.IsBold()


    def IsItalic(self, item):
        """
        Returns whether the item font is italic or not.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: ``True`` if the item has italic text, ``False`` otherwise.
        """

        return item.IsItalic()


# -----------------------------------------------------------------------------
# navigation
# -----------------------------------------------------------------------------

    def GetItemParent(self, item):
        """
        Returns the item parent (can be ``None`` for root items).

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: An instance of :class:`GenericTreeItem` or ``None`` for root items.
        """

        return item.GetParent()


    def GetFirstChild(self, item):
        """
        Returns the item's first child and an integer value 'cookie'.
        Call :meth:`~CustomTreeCtrl.GetNextChild` for the next child using this very 'cookie' return
        value as an input.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: A tuple with the first value being an instance of :class:`GenericTreeItem` or ``None`` if there are no
         further children, and as second value an integer parameter 'cookie'.

        :note: This method returns ``None`` if there are no further children.
        """

        cookie = 0
        return self.GetNextChild(item, cookie)


    def GetNextChild(self, item, cookie):
        """
        Returns the item's next child.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param `cookie`: a parameter which is opaque for the application but is necessary
         for the library to make these functions reentrant (i.e. allow more than one
         enumeration on one and the same object simultaneously).

        :return: A tuple with the first value being an instance of :class:`GenericTreeItem` or ``None`` if there are no
         further children, and as second value an integer parameter 'cookie'.

        :note: This method returns ``None`` if there are no further children.
        """

        children = item.GetChildren()

        # it's ok to cast cookie to size_t, we never have indices big enough to
        # overflow "void *"

        if cookie < len(children):

            return children[cookie], cookie+1

        else:

            # there are no more of them
            return None, cookie


    def GetLastChild(self, item):
        """
        Returns the item last child.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: An instance of :class:`GenericTreeItem` or ``None`` if there are no
         further children.
        """

        children = item.GetChildren()
        return (len(children) == 0 and [None] or [children[-1]])[0]


    def GetNextSibling(self, item):
        """
        Returns the next sibling of an item.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: An instance of :class:`GenericTreeItem` or ``None`` if there are no
         further siblings.

        :note: This method returns ``None`` if there are no further siblings.
        """

        parent = item.GetParent()

        if parent is None:
            # root item doesn't have any siblings
            return None

        siblings = parent.GetChildren()
        if item not in siblings:
            # Item is unlinked from tree
            return None

        index = siblings.index(item)
        n = index + 1
        return (n == len(siblings) and [None] or [siblings[n]])[0]


    def GetPrevSibling(self, item):
        """
        Returns the previous sibling of an item.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: An instance of :class:`GenericTreeItem` or ``None`` if there are no
         further siblings.

        :note: This method returns ``None`` if there are no further siblings.
        """

        parent = item.GetParent()

        if parent is None:
            # root item doesn't have any siblings
            return None

        siblings = parent.GetChildren()
        if item not in siblings:
            # Item is unlinked from tree
            return None

        index = siblings.index(item)
        return (index == 0 and [None] or [siblings[index-1]])[0]


    def GetNext(self, item):
        """
        Returns the next item. Only for internal use right now.

        :return: An instance of :class:`GenericTreeItem` or ``None`` if there are no
         further items.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        i = item

        # First see if there are any children.
        children = i.GetChildren()
        if len(children) > 0:
             return children[0]
        else:
             # Try a sibling of this or ancestor instead
             p = item
             toFind = None
             while p and not toFind:
                  toFind = self.GetNextSibling(p)
                  p = self.GetItemParent(p)

             return toFind


    def GetPrev(self, item):
        """
        Returns the previous item. Only for internal use right now.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: An instance of :class:`GenericTreeItem`
        """

        # Look for a previous sibling of this item
        prevSibling = self.GetPrevSibling(item)
        if prevSibling:

            # return it's last child or itself if has not got any children
            if len(prevSibling.GetChildren()) > 0:
                return self.GetLastChild(prevSibling)

            return prevSibling

        # item has not got a previous sibling, return it's parent
        return self.GetItemParent(item)


    def GetNextExpanded(self, item):
        """
        Returns the next expanded item after the input one.

        :param `item`: an instance of :class:`TreeListItem`.
        """

        nextSibling = self.GetNextSibling(item)
        if nextSibling:
            if nextSibling.IsExpanded():
                return nextSibling

            return self.GetNextExpanded(prevSibling)

        return None


    def GetPrevExpanded(self, item):
        """
        Returns the previous expanded item before the input one.

        :param `item`: an instance of :class:`TreeListItem`.
        """

        prevSibling = self.GetPrevSibling(item)
        if prevSibling:
            if prevSibling.IsExpanded():
                return prevSibling

            return self.GetPrevExpanded(prevSibling)

        return None


    def GetFirstVisibleItem(self):
        """
        Returns the first visible item.

        :return: An instance of :class:`GenericTreeItem` or ``None`` if there are no
         visible items.
        """

        id = self.GetRootItem()
        if not id:
            return id

        while id:
            if self.IsVisible(id):
                return id
            id = self.GetNext(id)

        return None


    def GetNextVisible(self, item):
        """
        Returns the next visible item.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: An instance of :class:`GenericTreeItem` or ``None`` if there are no
         next visible items.
        """

        id = item

        while id:
            id = self.GetNext(id)
            if id and self.IsVisible(id):
                return id

        return None


    def GetPrevVisible(self, item):
        """
        Returns the previous visible item.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: An instance of :class:`GenericTreeItem` or ``None`` if there are no
         previous visible items.
        """

        # find a previous sibling or parent which is visible
        lastGoodItem = self.GetPrevSibling(item)
        if not lastGoodItem or not self.IsVisible(lastGoodItem):
            parent = self.GetItemParent(item)
            rootHidden = self.HasAGWFlag(TR_HIDE_ROOT)
            rootItem = self.GetRootItem()

            while parent and not (rootHidden and parent == rootItem):
                if self.IsVisible(parent):
                    lastGoodItem = parent
                    break
                parent = self.GetItemParent(parent)

            if not lastGoodItem:
                return None

        # test if found item has visible children, if so and if the found item is not the
        # parent of the current item traverse the found item to the last visible child
        if not self.HasChildren(lastGoodItem) or not self.IsExpanded(lastGoodItem) or \
           (self.GetItemParent(item) == lastGoodItem):
            return lastGoodItem

        lastChild = self.GetLastChild(lastGoodItem)
        while lastChild and self.IsVisible(lastChild):
            lastGoodItem = lastChild
            lastChild = self.GetLastChild(lastGoodItem)

        return lastGoodItem


    def ResetEditControl(self):
        """ Called by :class:`TreeTextCtrl` when it marks itself for deletion. """

        if self._editCtrl is not None:
            self._editCtrl.Destroy()
            self._editCtrl = None

        self.CalculatePositions()
        self.Refresh()
        self.AdjustMyScrollbars()


    def FindItem(self, idParent, prefixOrig):
        """
        Finds the first item starting with the given prefix after the given parent.

        :param integer `idParent`: an instance of :class:`GenericTreeItem`;
        :param string `prefixOrig`: a string containing the item text prefix.

        :return: An instance of :class:`GenericTreeItem` or ``None`` if no item has been found.
        """

        # match is case insensitive as this is more convenient to the user: having
        # to press Shift-letter to go to the item starting with a capital letter
        # would be too bothersome
        prefix = prefixOrig.lower()

        # determine the starting point: we shouldn't take the current item (this
        # allows to switch between two items starting with the same letter just by
        # pressing it) but we shouldn't jump to the next one if the user is
        # continuing to type as otherwise he might easily skip the item he wanted
        id = idParent

        if len(prefix) == 1:
            id = self.GetNext(id)

        # look for the item starting with the given prefix after it
        while id and not self.GetItemText(id).lower().startswith(prefix):

            id = self.GetNext(id)

        # if we haven't found anything...
        if not id:

            # ... wrap to the beginning
            id = self.GetRootItem()
            if self.HasAGWFlag(TR_HIDE_ROOT):
                # can't select virtual root
                id = self.GetNext(id)
                if idParent == self.GetRootItem():
                    # no tree item selected and idParent is not reachable
                    return id

            # and try all the items (stop when we get to the one we started from)
            while id != idParent and not self.GetItemText(id).lower().startswith(prefix):
                id = self.GetNext(id)

        return id


# -----------------------------------------------------------------------------
# operations
# -----------------------------------------------------------------------------

    def DoInsertItem(self, parentId, previous, text, ct_type=0, wnd=None, image=-1, selImage=-1, data=None, separator=False, on_the_right=True):
        """
        Actually inserts an item in the tree.

        :param `parentId`: an instance of :class:`GenericTreeItem` representing the
         item's parent;
        :param integer `previous`: the index at which we should insert the item;
        :param string `text`: the item text label;
        :param integer `ct_type`: the item type (see :meth:`~CustomTreeCtrl.SetItemType` for a list of valid
         item types);
        :param `wnd`: if not ``None``, a non-toplevel window to show next to the item, any
         subclass of :class:`wx.Window` except top-level windows;
        :param integer `image`: an index within the normal image list specifying the image to
         use for the item in unselected state;
        :param integer `selImage`: an index within the normal image list specifying the image to
         use for the item in selected state; if `image` > -1 and `selImage` is -1, the
         same image is used for both selected and unselected items;
        :param object `data`: associate the given Python object `data` with the item;
        :param bool `separator`: ``True`` if the item is a separator, ``False`` otherwise.
        :param bool `on_the_right`: ``True`` positions the window on the right of text, ``False``
         on the left of text and overlapping the image.

        :return: An instance of :class:`GenericTreeItem` upon successful insertion.

        :raise: `Exception` in the following cases:

         - The item window is not ``None`` but the ``TR_HAS_VARIABLE_ROW_HEIGHT`` flag has not been
           set for :class:`CustomTreeCtrl`;
         - The item has multiline text (with line-breaks in it) but the ``TR_HAS_VARIABLE_ROW_HEIGHT``
           flag has not been set for :class:`CustomTreeCtrl`;
         - The `ct_type` attribute is less than ``0`` or greater than ``2``;
         - The parent item is a separator;
         - The item is a separator but it has text or an associated window.


        :note: Separator items should not have children, text labels or an associated window.
        """

        if wnd is not None and not self.HasAGWFlag(TR_HAS_VARIABLE_ROW_HEIGHT):
            raise Exception("\nERROR: In Order To Append/Insert Controls You Have To Use The Style TR_HAS_VARIABLE_ROW_HEIGHT")

        if text.find("\n") >= 0 and not self.HasAGWFlag(TR_HAS_VARIABLE_ROW_HEIGHT):
            raise Exception("\nERROR: In Order To Append/Insert A MultiLine Text You Have To Use The Style TR_HAS_VARIABLE_ROW_HEIGHT")

        if ct_type < 0 or ct_type > 2:
            raise Exception("\nERROR: Item Type Should Be 0 (Normal), 1 (CheckBox) or 2 (RadioButton). ")

        if separator:
            if wnd:
                raise Exception("Separator items can not have associated windows")
            if text.strip():
                raise Exception("Separator items can not text labels")

        parent = parentId

        if not parent:
            # should we give a warning here?
            return self.AddRoot(text, ct_type, wnd, image, selImage, data)

        self._dirty = True     # do this first so stuff below doesn't cause flicker

        item = GenericTreeItem(parent, text, ct_type, wnd, image, selImage, data, separator, on_the_right)

        if wnd is not None:
            self._hasWindows = True
            self._itemWithWindow.append(item)

        parent.Insert(item, previous)

        return item


    def AddRoot(self, text, ct_type=0, wnd=None, image=-1, selImage=-1, data=None, on_the_right=True):
        """
        Adds a root item to the :class:`CustomTreeCtrl`.

        :param string `text`: the item text label;
        :param integer `ct_type`: the item type (see :meth:`~CustomTreeCtrl.SetItemType` for a list of valid
         item types);
        :param `wnd`: if not ``None``, a non-toplevel window to show next to the item,
         any subclass of :class:`wx.Window` except top-level windows;
        :param integer `image`: an index within the normal image list specifying the image to
         use for the item in unselected state;
        :param  integer `selImage`: an index within the normal image list specifying the image to
         use for the item in selected state; if `image` > -1 and `selImage` is -1, the
         same image is used for both selected and unselected items;
        :param object `data`: associate the given Python object `data` with the item.
        :param bool `on_the_right`: ``True`` positions the window on the right of text, ``False``
         on the left of text and overlapping the image.

        :return: An instance of :class:`GenericTreeItem` upon successful insertion.

        :raise: `Exception` in the following cases:

         - There already is a root item in the tree;
         - The item window is not ``None`` but the ``TR_HAS_VARIABLE_ROW_HEIGHT`` flag has not been
           set for :class:`CustomTreeCtrl`;
         - The item has multiline text (with line-breaks in it) but the ``TR_HAS_VARIABLE_ROW_HEIGHT``
           flag has not been set for :class:`CustomTreeCtrl`;
         - The `ct_type` attribute is less than ``0`` or greater than ``2``.

        .. warning::

           Only one root is allowed to exist in any given instance of :class:`CustomTreeCtrl`.

        """

        if self._anchor:
            raise Exception("\nERROR: Tree Can Have Only One Root")

        if wnd is not None and not self.HasAGWFlag(TR_HAS_VARIABLE_ROW_HEIGHT):
            raise Exception("\nERROR: In Order To Append/Insert Controls You Have To Use The Style TR_HAS_VARIABLE_ROW_HEIGHT")

        if text.find("\n") >= 0 and not self.HasAGWFlag(TR_HAS_VARIABLE_ROW_HEIGHT):
            raise Exception("\nERROR: In Order To Append/Insert A MultiLine Text You Have To Use The Style TR_HAS_VARIABLE_ROW_HEIGHT")

        if ct_type < 0 or ct_type > 2:
            raise Exception("\nERROR: Item Type Should Be 0 (Normal), 1 (CheckBox) or 2 (RadioButton). ")

        self._dirty = True     # do this first so stuff below doesn't cause flicker

        self._anchor = GenericTreeItem(None, text, ct_type=ct_type, wnd=wnd,
                                       image=image, selImage=selImage,
                                       data=data, on_the_right=on_the_right)

        if wnd is not None:
            self._hasWindows = True
            self._itemWithWindow.append(self._anchor)

        if self.HasAGWFlag(TR_HIDE_ROOT):

            # if root is hidden, make sure we can navigate
            # into children
            self._anchor.SetHasPlus()
            self._anchor.Expand()
            self.CalculatePositions()

        if not self.HasAGWFlag(TR_MULTIPLE):

            self._current = self._key_current = self._anchor
            self._current.SetHilight(True)

        return self._anchor


    def PrependItem(self, parent, text, ct_type=0, wnd=None, image=-1, selImage=-1, data=None, separator=False, on_the_right=True):
        """
        Prepends an item as a first child of parent.

        :param `parent`: an instance of :class:`GenericTreeItem` representing the
         item's parent;
        :param string `text`: the item text label;
        :param integer `ct_type`: the item type (see :meth:`~CustomTreeCtrl.SetItemType` for a list of valid
         item types);
        :param `wnd`: if not ``None``, a non-toplevel window to show next to the item, any
         subclass of :class:`wx.Window` except top-level windows;
        :param integer `image`: an index within the normal image list specifying the image to
         use for the item in unselected state;
        :param integer `selImage`: an index within the normal image list specifying the image to
         use for the item in selected state; if `image` > -1 and `selImage` is -1, the
         same image is used for both selected and unselected items;
        :param object `data`: associate the given Python object `data` with the item;
        :param bool `separator`: ``True`` if the item is a separator, ``False`` otherwise.
        :param bool `on_the_right`: ``True`` positions the window on the right of text, ``False``
         on the left of text and overlapping the image.

        :return: An instance of :class:`GenericTreeItem` upon successful insertion.

        :see: :meth:`~CustomTreeCtrl.DoInsertItem` for possible exceptions generated by this method.
        """

        return self.DoInsertItem(parent, 0, text, ct_type, wnd, image, selImage, data, separator, on_the_right)


    def InsertItemByItem(self, parentId, idPrevious, text, ct_type=0, wnd=None, image=-1, selImage=-1, data=None, separator=False, on_the_right=True):
        """
        Inserts an item after the given previous.

        :param `parentId`: an instance of :class:`GenericTreeItem` representing the
         item's parent;
        :param `idPrevious`: an instance of :class:`GenericTreeItem` representing the
         previous item;
        :param string `text`: the item text label;
        :param integer `ct_type`: the item type (see :meth:`~CustomTreeCtrl.SetItemType` for a list of valid
         item types);
        :param `wnd`: if not ``None``, a non-toplevel window to show next to the item,
         any subclass of :class:`wx.Window`;
        :param integer `image`: an index within the normal image list specifying the image to
         use for the item in unselected state;
        :param integer `selImage`: an index within the normal image list specifying the image to
         use for the item in selected state; if `image` > -1 and `selImage` is -1, the
         same image is used for both selected and unselected items;
        :param object `data`: associate the given Python object `data` with the item;
        :param bool `separator`: ``True`` if the item is a separator, ``False`` otherwise.
        :param bool `on_the_right`: ``True`` positions the window on the right of text, ``False``
         on the left of text and overlapping the image.

        :return: An instance of :class:`GenericTreeItem` upon successful insertion.

        :raise: `Exception` if the previous item is not a sibling.

        :see: :meth:`~CustomTreeCtrl.DoInsertItem` for other possible exceptions generated by this method.
        """

        parent = parentId

        if not parent:
            # should we give a warning here?
            return self.AddRoot(text, ct_type, wnd, image, selImage, data, on_the_right)

        index = -1
        if idPrevious:

            try:
                index = parent.GetChildren().index(idPrevious)
            except:
                raise Exception("ERROR: Previous Item In CustomTreeCtrl.InsertItem() Is Not A Sibling")

        return self.DoInsertItem(parentId, index+1, text, ct_type, wnd, image, selImage, data, separator, on_the_right)


    def InsertItemByIndex(self, parentId, idPrevious, text, ct_type=0, wnd=None, image=-1, selImage=-1, data=None, separator=False, on_the_right=True):
        """
        Inserts an item after the given previous.

        :param `parentId`: an instance of :class:`GenericTreeItem` representing the
         item's parent;
        :param `idPrevious`: the index at which we should insert the new item;
        :param string `text`: the item text label;
        :param integer `ct_type`: the item type (see :meth:`~CustomTreeCtrl.SetItemType` for a list of valid
         item types);
        :param `wnd`: if not ``None``, a non-toplevel window to show next to the item,
         any subclass of :class:`wx.Window`;
        :param integer `image`: an index within the normal image list specifying the image to
         use for the item in unselected state;
        :param integer `selImage`: an index within the normal image list specifying the image to
         use for the item in selected state; if `image` > -1 and `selImage` is -1, the
         same image is used for both selected and unselected items;
        :param object `data`: associate the given Python object `data` with the item;
        :param bool `separator`: ``True`` if the item is a separator, ``False`` otherwise.
        :param bool `on_the_right`: ``True`` positions the window on the right of text, ``False``
         on the left of text and overlapping the image.

        :return: An instance of :class:`GenericTreeItem` upon successful insertion.

        :see: :meth:`~CustomTreeCtrl.DoInsertItem` for possible exceptions generated by this method.
        """

        parent = parentId

        if not parent:
            # should we give a warning here?
            return self.AddRoot(text, ct_type, wnd, image, selImage, data)

        return self.DoInsertItem(parentId, idPrevious, text, ct_type, wnd, image, selImage, data, separator, on_the_right)


    def InsertItem(self, parentId, input, text, ct_type=0, wnd=None, image=-1, selImage=-1, data=None, separator=False, on_the_right=True):
        """
        Inserts an item after the given previous.

        :return: An instance of :class:`GenericTreeItem` upon successful insertion.

        :see: :meth:`~CustomTreeCtrl.InsertItemByIndex` and :meth:`~CustomTreeCtrl.InsertItemByItem` for an explanation of
         the input parameters.

        :see: :meth:`~CustomTreeCtrl.DoInsertItem` for possible exceptions generated by this method.
        """

        if type(input) == type(1):
            return self.InsertItemByIndex(parentId, input, text, ct_type, wnd, image, selImage, data, separator, on_the_right)
        else:
            return self.InsertItemByItem(parentId, input, text, ct_type, wnd, image, selImage, data, separator, on_the_right)


    def AppendItem(self, parentId, text, ct_type=0, wnd=None, image=-1, selImage=-1, data=None, on_the_right=True):
        """
        Appends an item as a last child of its parent.

        :param `parentId`: an instance of :class:`GenericTreeItem` representing the
         item's parent;
        :param string `text`: the item text label;
        :param integer `ct_type`: the item type (see :meth:`~CustomTreeCtrl.SetItemType` for a list of valid
         item types);
        :param `wnd`: if not ``None``, a non-toplevel window to show next to the item,
         any subclass of :class:`wx.Window`;
        :param integer `image`: an index within the normal image list specifying the image to
         use for the item in unselected state;
        :param integer `selImage`: an index within the normal image list specifying the image to
         use for the item in selected state; if `image` > -1 and `selImage` is -1, the
         same image is used for both selected and unselected items;
        :param object `data`: associate the given Python object `data` with the item.
        :param bool `on_the_right`: ``True`` positions the window on the right of text, ``False``
         on the left of text and overlapping the image.

        :return: An instance of :class:`GenericTreeItem` upon successful insertion.

        :see: :meth:`~CustomTreeCtrl.DoInsertItem` for possible exceptions generated by this method.
        """

        parent = parentId

        if not parent:
            # should we give a warning here?
            return self.AddRoot(text, ct_type, wnd, image, selImage, data, on_the_right)

        return self.DoInsertItem(parent, len(parent.GetChildren()), text, ct_type, wnd, image, selImage, data, False, on_the_right)


    def AppendSeparator(self, parentId):
        """
        Appends an horizontal line separator as a last child of its parent.

        :param `parentId`: an instance of :class:`GenericTreeItem` representing the
         separator's parent.

        :return: An instance of :class:`GenericTreeItem` upon successful insertion.

        :see: :meth:`~CustomTreeCtrl.DoInsertItem` for possible exceptions generated by this method.
        """

        parent = parentId
        return self.DoInsertItem(parent, len(parent.GetChildren()), "", separator=True)


    def InsertSeparator(self, parentId, input):
        """
        Inserts a separator item after the given previous.

        :return: An instance of :class:`GenericTreeItem` upon successful insertion.

        :see: :meth:`~CustomTreeCtrl.InsertItemByIndex` and :meth:`~CustomTreeCtrl.InsertItemByItem` for an explanation of
         the input parameters.

        :see: :meth:`~CustomTreeCtrl.DoInsertItem` for possible exceptions generated by this method.
        """

        return self.InsertItem(parentId, input, "", separator=True)


    def PrependSeparator(self, parent):
        """
        Prepends a separator item as a first child of parent.

        :param `parent`: an instance of :class:`GenericTreeItem` representing the
         item's parent.

        :return: An instance of :class:`GenericTreeItem` upon successful insertion.

        :see: :meth:`~CustomTreeCtrl.DoInsertItem` for possible exceptions generated by this method.
        """

        return self.PrependItem(parent, 0, separator=True)


    def SendDeleteEvent(self, item):
        """
        Actually sends the ``EVT_TREE_DELETE_ITEM`` event.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        event = TreeEvent(wxEVT_TREE_DELETE_ITEM, self.GetId())
        event._item = item
        event.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(event)


    def IsDescendantOf(self, parent, item):
        """
        Checks if the given item is under another one in the tree hierarchy.

        :param `parent`: an instance of :class:`GenericTreeItem`, representing the possible
         parent of `item`;
        :param `item`: another instance of :class:`GenericTreeItem`.

        :return: ``True`` if `item` is a descendant of `parent`, ``False`` otherwise.
        """

        while item:

            if item == parent:

                # item is a descendant of parent
                return True

            item = item.GetParent()

        return False


    # Don't leave edit or selection on a child which is about to disappear
    def ChildrenClosing(self, item):
        """
        We are about to destroy the item children.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        if self._editCtrl is not None and item != self._editCtrl.item() and self.IsDescendantOf(item, self._editCtrl.item()):
            self._editCtrl.StopEditing()

        if item != self._key_current and self.IsDescendantOf(item, self._key_current):
            self._key_current = None

        if self.IsDescendantOf(item, self._select_me):
            self._select_me = item

        if item != self._current and self.IsDescendantOf(item, self._current):
            self._current.SetHilight(False)
            self._current = None
            self._select_me = item


    def DeleteChildren(self, item):
        """
        Delete all the item's children.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        self._dirty = True     # do this first so stuff below doesn't cause flicker

        self.ChildrenClosing(item)
        item.DeleteChildren(self)


    def Delete(self, item):
        """
        Deletes an item.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :note: This method sends the ``EVT_TREE_DELETE_ITEM`` event.
        """

        self._dirty = True     # do this first so stuff below doesn't cause flicker

        if self._editCtrl is not None and self.IsDescendantOf(item, self._editCtrl.item()):
            # can't delete the item being edited, cancel editing it first
            self._editCtrl.StopEditing()

        parent = item.GetParent()

        # don't keep stale pointers around!
        if self.IsDescendantOf(item, self._key_current):

            # Don't silently change the selection:
            # do it properly in idle time, so event
            # handlers get called.

            # self._key_current = parent
            self._key_current = None

        # self._select_me records whether we need to select
        # a different item, in idle time.
        if self._select_me and self.IsDescendantOf(item, self._select_me):
            self._select_me = parent

        if self.IsDescendantOf(item, self._current):

            # Don't silently change the selection:
            # do it properly in idle time, so event
            # handlers get called.

            # self._current = parent
            self._current = None
            self._select_me = parent

        # remove the item from the tree
        if parent:

            parent.GetChildren().remove(item)  # remove by value

        else: # deleting the root

            # nothing will be left in the tree
            self._anchor = None

        # and delete all of its children and the item itself now
        item.DeleteChildren(self)
        self.SendDeleteEvent(item)

        if item == self._select_me:
            self._select_me = None

        # Remove the item with window
        if item in self._itemWithWindow:
            wnd = item.GetWindow()
            wnd.Hide()
            wnd.Destroy()
            item._wnd = None
            self._itemWithWindow.remove(item)

        del item


    def DeleteAllItems(self):
        """ Deletes all items in the :class:`CustomTreeCtrl`. """

        if self._anchor:
            self.Delete(self._anchor)


    def Expand(self, item):
        """
        Expands an item, sending a ``EVT_TREE_ITEM_EXPANDING`` and
        ``EVT_TREE_ITEM_EXPANDED`` events.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :raise: `Exception` if you try to expand a hidden root (i.e., when the ``TR_HIDE_ROOT``
         style is set for :class:`CustomTreeCtrl`).
        """

        if self.HasAGWFlag(TR_HIDE_ROOT) and item == self.GetRootItem():
             raise Exception("\nERROR: Can't Expand An Hidden Root. ")

        if not item.HasPlus():
            return

        if item.IsExpanded():
            return

        if self._sendEvent:
            event = TreeEvent(wxEVT_TREE_ITEM_EXPANDING, self.GetId())
            event._item = item
            event.SetEventObject(self)

            if self.GetEventHandler().ProcessEvent(event) and not event.IsAllowed():
                # cancelled by program
                return

        item.Expand()

        if not self._sendEvent:
            # We are in ExpandAll/ExpandAllChildren
            return

        self.CalculatePositions()
        self.RefreshSubtree(item)

        if self._hasWindows:
            # We hide the associated window here, we may show it after
            self.HideWindows()

        event.SetEventType(wxEVT_TREE_ITEM_EXPANDED)
        self.GetEventHandler().ProcessEvent(event)


    def ExpandAllChildren(self, item):
        """
        Expands all the items children of the input item.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :note: This method suppresses the ``EVT_TREE_ITEM_EXPANDING`` and
         ``EVT_TREE_ITEM_EXPANDED`` events because expanding many items int the
         control would be too slow then.
        """

        self._sendEvent = False
        if not self.HasAGWFlag(TR_HIDE_ROOT) or item != self.GetRootItem():
            self.Expand(item)
            if not self.IsExpanded(item):
                self._sendEvent = True
                return

        child, cookie = self.GetFirstChild(item)

        while child:
            self.ExpandAllChildren(child)
            child, cookie = self.GetNextChild(item, cookie)

        self._sendEvent = True
        self._dirty = True


    def ExpandAll(self):
        """
        Expands all :class:`CustomTreeCtrl` items.

        :note: This method suppresses the ``EVT_TREE_ITEM_EXPANDING`` and
         ``EVT_TREE_ITEM_EXPANDED`` events because expanding many items int the
         control would be too slow then.
        """

        if self._anchor:
            self.ExpandAllChildren(self._anchor)

        self._sendEvent = True
        self._dirty = True


    def Collapse(self, item):
        """
        Collapse an item, sending a ``EVT_TREE_ITEM_COLLAPSING`` and
        ``EVT_TREE_ITEM_COLLAPSED`` events.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :raise: `Exception` if you try to collapse a hidden root (i.e., when the ``TR_HIDE_ROOT``
         style is set for :class:`CustomTreeCtrl`).
        """

        if self.HasAGWFlag(TR_HIDE_ROOT) and item == self.GetRootItem():
             raise Exception("\nERROR: Can't Collapse An Hidden Root. ")

        if not item.IsExpanded():
            return

        event = TreeEvent(wxEVT_TREE_ITEM_COLLAPSING, self.GetId())
        event._item = item
        event.SetEventObject(self)
        if self.GetEventHandler().ProcessEvent(event) and not event.IsAllowed():
            # cancelled by program
            return

        self.ChildrenClosing(item)
        item.Collapse()

        self.CalculatePositions()
        self.Refresh()

        if self._hasWindows:
            self.HideWindows()

        self.AdjustMyScrollbars()

        event.SetEventType(wxEVT_TREE_ITEM_COLLAPSED)
        self.GetEventHandler().ProcessEvent(event)


    def CollapseAndReset(self, item):
        """
        Collapse the given item and deletes its children.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        self.Collapse(item)
        self.DeleteChildren(item)


    def Toggle(self, item):
        """
        Toggles the item state (collapsed/expanded).

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        if item.IsExpanded():
            self.Collapse(item)
        else:
            self.Expand(item)


    def HideWindows(self):
        """ Hides the windows associated to the items. Used internally. """

        for child in self._itemWithWindow:
            if not self.IsVisible(child):
                wnd = child.GetWindow()
                if wnd:
                    wnd.Hide()


    def HideItemWindows(self, item):
        """Hide all windows belonging to the item and its children."""
        wnd = item.GetWindow()
        if wnd:
            wnd.Hide()
        for child in item.GetChildren():
            self.HideItemWindows(child)            


    def HideItem(self, item, hide=True):
        """
        Hides/shows an item.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param `hide`: ``True`` to hide the item, ``False`` to show it.

        :note: A hidden item always reports that it is collapsed and disabled.
        """
        if hide == item.IsHidden():
            # Item already in correct state. Don't do anything.
            return
        item.Hide(hide)

        if hide is True and self._hasWindows:
            # Hide all windows for this item and its children.
            self.HideItemWindows(item)

        # Refresh the tree.
        self.CalculatePositions()
        self.Refresh()
        self.AdjustMyScrollbars()


    def Unselect(self):
        """ Unselects the current selection. """

        if self._current:
            self._current.SetHilight(False)
            self.RefreshLine(self._current)

        self._current = None
        self._select_me = None


    def UnselectAllChildren(self, item):
        """
        Unselects all the children of the given item.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        if item.IsSelected():
            item.SetHilight(False)
            self.RefreshLine(item)

        if item.HasChildren():
            for child in item.GetChildren():
                self.UnselectAllChildren(child)


    def SelectAllChildren(self, item):
        """
        Selects all the children of the given item.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :raise: `Exception` if used without the ``TR_EXTENDED`` or ``TR_MULTIPLE`` style set.

        :note: This method can be used only if :class:`CustomTreeCtrl` has the ``TR_MULTIPLE`` or ``TR_EXTENDED``
         style set.
        """

        if not self.HasAGWFlag(TR_MULTIPLE) and not self.HasAGWFlag(TR_EXTENDED):
            raise Exception("SelectAllChildren can be used only with multiple selection enabled.")

        if not item.IsSelected():
            item.SetHilight(True)
            self.RefreshLine(item)

        if item.HasChildren():
            for child in item.GetChildren():
                self.SelectAllChildren(child)


    def UnselectAll(self):
        """ Unselect all the items. """

        rootItem = self.GetRootItem()

        # the tree might not have the root item at all
        if rootItem:
            self.UnselectAllChildren(rootItem)

        self.Unselect()


    def SelectAll(self):
        """
        Selects all the item in the tree.

        :raise: `Exception` if used without the ``TR_EXTENDED`` or ``TR_MULTIPLE`` style set.

        :note: This method can be used only if :class:`CustomTreeCtrl` has the ``TR_MULTIPLE`` or ``TR_EXTENDED``
         style set.
        """

        if not self.HasAGWFlag(TR_MULTIPLE) and not self.HasAGWFlag(TR_EXTENDED):
            raise Exception("SelectAll can be used only with multiple selection enabled.")

        rootItem = self.GetRootItem()

        # the tree might not have the root item at all
        if rootItem:
            self.SelectAllChildren(rootItem)


    # Recursive function !
    # To stop we must have crt_item<last_item
    # Algorithm :
    # Tag all next children, when no more children,
    # Move to parent (not to tag)
    # Keep going... if we found last_item, we stop.

    def TagNextChildren(self, crt_item, last_item, select):
        """ Used internally. """

        parent = crt_item.GetParent()

        if parent is None: # This is root item
            return self.TagAllChildrenUntilLast(crt_item, last_item, select)

        children = parent.GetChildren()
        index = children.index(crt_item)

        count = len(children)

        for n in range(index+1, count):
            if self.TagAllChildrenUntilLast(children[n], last_item, select):
                return True

        return self.TagNextChildren(parent, last_item, select)


    def TagAllChildrenUntilLast(self, crt_item, last_item, select):
        """ Used internally. """

        crt_item.SetHilight(select)
        self.RefreshLine(crt_item)

        if crt_item == last_item:
            return True

        if crt_item.HasChildren():
            for child in crt_item.GetChildren():
                if self.TagAllChildrenUntilLast(child, last_item, select):
                    return True

        return False


    def SelectItemRange(self, item1, item2):
        """
        Selects all the items between `item1` and `item2`.

        :param `item1`: an instance of :class:`GenericTreeItem`, representing the first
         item in the range to select;
        :param `item2`: an instance of :class:`GenericTreeItem`, representing the last
         item in the range to select.

        :raise: `Exception` if used without the ``TR_EXTENDED`` or ``TR_MULTIPLE`` style set.

        :note: This method can be used only if :class:`CustomTreeCtrl` has the ``TR_MULTIPLE`` or ``TR_EXTENDED``
         style set.
        """

        if not self.HasAGWFlag(TR_MULTIPLE) and not self.HasAGWFlag(TR_EXTENDED):
            raise Exception("SelectItemRange can be used only with multiple selection enabled.")

        self._select_me = None

        # item2 is not necessary after item1
        # choice first' and 'last' between item1 and item2
        first = (item1.GetY() < item2.GetY() and [item1] or [item2])[0]
        last = (item1.GetY() < item2.GetY() and [item2] or [item1])[0]

        select = self._current.IsSelected()

        if self.TagAllChildrenUntilLast(first, last, select):
            return

        self.TagNextChildren(first, last, select)


    def DoSelectItem(self, item, unselect_others=True, extended_select=False, from_key=False):
        """
        Actually selects/unselects an item, sending ``EVT_TREE_SEL_CHANGING`` and
        ``EVT_TREE_SEL_CHANGED`` events.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `unselect_others`: if ``True``, all the other selected items are
         unselected.
        :param bool `extended_select`: ``True`` if the :class:`CustomTreeCtrl` is using the
         ``TR_EXTENDED`` style;
        :param bool `from_key`: ``True`` to indicate that the selection was made via a keyboard
         key, ``False`` if it was a mouse selection.
        """

        self._select_me = None

        is_single = not (self.GetAGWWindowStyleFlag() & TR_MULTIPLE)

        # to keep going anyhow !!!
        if is_single:
            if item.IsSelected() and not from_key:
                # Handles hypertext items
                self.HandleHyperLink(item)
                return # nothing else to do
            unselect_others = True
            extended_select = False

        elif unselect_others and item.IsSelected():

            # selection change if there is more than one item currently selected
            if len(self.GetSelections()) == 1 and not from_key:
                # Handles hypertext items
                self.HandleHyperLink(item)
                return

        event = TreeEvent(wxEVT_TREE_SEL_CHANGING, self.GetId())
        event._item = item
        event._itemOld = self._current
        event.SetEventObject(self)
        # TODO : Here we don't send any selection mode yet !

        if self.GetEventHandler().ProcessEvent(event) and not event.IsAllowed():
            return

        parent = self.GetItemParent(item)
        while parent:
            if not self.IsExpanded(parent):
                self.Expand(parent)

            parent = self.GetItemParent(parent)

        # ctrl press
        if unselect_others:
            if is_single:
                self.Unselect() # to speed up thing
            else:
                self.UnselectAll()

        # shift press
        if extended_select:
            if not self._current:
                self._current = self._key_current = self.GetRootItem()

            # don't change the mark (self._current)
            self.SelectItemRange(self._current, item)

        else:

            select = True # the default

            # Check if we need to toggle highlight (ctrl mode)
            if not unselect_others:
                select = not item.IsSelected()

            self._current = self._key_current = item
            self._current.SetHilight(select)
            self.RefreshLine(self._current)

        # This can cause idle processing to select the root
        # if no item is selected, so it must be after the
        # selection is set
        self.EnsureVisible(item)

        event.SetEventType(wxEVT_TREE_SEL_CHANGED)
        self.GetEventHandler().ProcessEvent(event)

        if not from_key:
            # Handles hypertext items
            self.HandleHyperLink(item)


    def SelectItem(self, item, select=True):
        """
        Selects/deselects an item.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `select`: ``True`` to select an item, ``False`` to deselect it.

        :note: If TR_MULTIPLE is set, this actually toggles selection when select=True.
        """

        if select:

            self.DoSelectItem(item, not self.HasAGWFlag(TR_MULTIPLE))

        else: # deselect

            item.SetHilight(False)
            self.RefreshLine(item)


    def FillArray(self, item, array=[]):
        """
        Internal function. Used to populate an array of selected items when
        the style ``TR_MULTIPLE`` is used.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param list `array`: a Python list containing the selected items.

        :return: A Python list containing the selected items.
        """

        if not array:
            array = []

        if item.IsSelected():
            array.append(item)

        if item.HasChildren() and item.IsExpanded():
            for child in item.GetChildren():
                array = self.FillArray(child, array)

        return array


    def GetSelections(self):
        """
        Returns a list of selected items.

        :note: This method can be used only if :class:`CustomTreeCtrl` has the ``TR_MULTIPLE`` or ``TR_EXTENDED``
         style set.

        :return: A Python list containing the selected items, all instances of :class:`GenericTreeItem`.
        """

        array = []
        idRoot = self.GetRootItem()
        if idRoot:
            array = self.FillArray(idRoot, array)

        #else: the tree is empty, so no selections

        return array


    def HandleHyperLink(self, item):
        """
        Handles the hyperlink items, sending the ``EVT_TREE_ITEM_HYPERLINK`` event.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        if self.IsItemHyperText(item):
            event = TreeEvent(wxEVT_TREE_ITEM_HYPERLINK, self.GetId())
            event._item = item
            self.GetEventHandler().ProcessEvent(event)


    def EnsureVisible(self, item):
        """
        Scrolls and/or expands items to ensure that the given item is visible.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        # first expand all parent branches
        parent = item.GetParent()

        if self.HasAGWFlag(TR_HIDE_ROOT):
            while parent and parent != self._anchor:
                self.Expand(parent)
                parent = parent.GetParent()
        else:
            while parent:
                self.Expand(parent)
                parent = parent.GetParent()

        self.ScrollTo(item)


    def ScrollTo(self, item):
        """
        Scrolls the specified item into view.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        if not item:
            return

        # We have to call this here because the label in
        # question might just have been added and no screen
        # update taken place.
        if self._dirty:
            if wx.Platform in ["__WXMSW__", "__WXMAC__"]:
                self.Update()
        else:
            wx.YieldIfNeeded()

        # now scroll to the item
        item_y = item.GetY()
        start_x, start_y = self.GetViewStart()
        start_y *= _PIXELS_PER_UNIT
        client_w, client_h = self.GetClientSize()

        # Calculate size of entire tree (not necessary anymore?)
        x, y = self._anchor.GetSize(0, 0, self)
        y += _PIXELS_PER_UNIT + 2 # one more scrollbar unit + 2 pixels
        x += _PIXELS_PER_UNIT + 2 # one more scrollbar unit + 2 pixels
        x_pos = self.GetScrollPos(wx.HORIZONTAL)

        ## Note: The Scroll() method updates all child window positions
        ##       while the SetScrollBars() does not (on most platforms).
        if item_y < start_y+3:
            # going down, item should appear at top
            self.Scroll(x_pos, item_y // _PIXELS_PER_UNIT)
            #self.SetScrollbars(_PIXELS_PER_UNIT, _PIXELS_PER_UNIT, x//_PIXELS_PER_UNIT, y//_PIXELS_PER_UNIT, x_pos, item_y//_PIXELS_PER_UNIT)

        elif item_y+self.GetLineHeight(item) > start_y+client_h:
            # going up, item should appear at bottom
            item_y += _PIXELS_PER_UNIT+2
            self.Scroll(x_pos, (item_y + self.GetLineHeight(item) - client_h) // _PIXELS_PER_UNIT)
            #self.SetScrollbars(_PIXELS_PER_UNIT, _PIXELS_PER_UNIT, x//_PIXELS_PER_UNIT, y//_PIXELS_PER_UNIT, x_pos, (item_y+self.GetLineHeight(item)-client_h)//_PIXELS_PER_UNIT )


    def OnCompareItems(self, item1, item2):
        """
        Returns whether 2 items have the same text.

        Override this function in the derived class to change the sort order of the items
        in the :class:`CustomTreeCtrl`. The function should return a negative, zero or positive
        value if the first item is less than, equal to or greater than the second one.

        :param `item1`: an instance of :class:`GenericTreeItem`;
        :param `item2`: another instance of :class:`GenericTreeItem`.

        :return: The return value is negative if `item1` < `item2`, zero if `item1` == `item2`
         and strictly positive if `item1` < `item2`.

        :note: The base class version compares items alphabetically.
        """

        a = self.GetItemText(item1)
        b = self.GetItemText(item2)
        return (a > b) - (a < b)  # equivalent to old cmp function


    def SortChildren(self, item):
        """
        Sorts the children of the given item using the :meth:`~CustomTreeCtrl.OnCompareItems` method of
        :class:`CustomTreeCtrl`.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :note: You should override the :meth:`~CustomTreeCtrl.OnCompareItems` method in your derived class to change
         the sort order (the default is ascending case-sensitive alphabetical order).
        """

        children = item.GetChildren()

        if len(children) > 1:
            self._dirty = True
            from functools import cmp_to_key
            children.sort(key=cmp_to_key(self.OnCompareItems))


    def GetImageList(self):
        """
        Returns the normal image list associated with :class:`CustomTreeCtrl`.

        :return: An instance of :class:`wx.ImageList`.
        """

        return self._imageListNormal


    def GetButtonsImageList(self):
        """
        Returns the buttons image list associated with :class:`CustomTreeCtrl` (from
        which application-defined button images are taken).

        :return: An instance of :class:`wx.ImageList`.
        """

        return self._imageListButtons


    def GetStateImageList(self):
        """
        Returns the state image list associated with :class:`CustomTreeCtrl` (from which
        application-defined state images are taken).

        :return: An instance of :class:`wx.ImageList`.
        """

        return self._imageListState


    def GetImageListCheck(self):
        """
        Returns the image list used to build the check/radio buttons in :class:`CustomTreeCtrl`.

        :return: An instance of :class:`wx.ImageList`.
        """

        return self._imageListCheck


    def GetLeftImageList(self):
        """
        Returns the image list for :class:`CustomTreeCtrl` filled with images to be used on
        the leftmost part of the client area. Any item can have a leftmost image associated
        with it.

        :return: An instance of :class:`wx.ImageList`.
        """

        return self._imageListLeft


    def CalculateLineHeight(self):
        """Calculates the base height for all lines in the tree.

        Only used if the TR_HAS_VARIABLE_ROW_HEIGHT style is not used.
        This base line height gets adjusted to the max line height
        of all items as they are displayed. All rows use this largest
        height until this method is called to reset it.
        """

        dc = wx.ClientDC(self)
        self._lineHeight = dc.GetCharHeight()

        if self._imageListNormal:

            # Calculate a self._lineHeight value from the normal Image sizes.
            # May be toggle off. Then CustomTreeCtrl will spread when
            # necessary (which might look ugly).
            n = self._imageListNormal.GetImageCount()

            for i in range(n):

                width, height = self._imageListNormal.GetSize(i)

                if height > self._lineHeight:
                    self._lineHeight = height

        if self._imageListButtons:

            # Calculate a self._lineHeight value from the Button image sizes.
            # May be toggle off. Then CustomTreeCtrl will spread when
            # necessary (which might look ugly).
            n = self._imageListButtons.GetImageCount()

            for i in range(n):

                width, height = self._imageListButtons.GetSize(i)

                if height > self._lineHeight:
                    self._lineHeight = height

        if self._imageListCheck:

            # Calculate a self._lineHeight value from the check/radio image sizes.
            # May be toggle off. Then CustomTreeCtrl will spread when
            # necessary (which might look ugly).
            n = self._imageListCheck.GetImageCount()

            for i in range(n):

                width, height = self._imageListCheck.GetSize(i)

                if height > self._lineHeight:
                    self._lineHeight = height

        if self._imageListLeft:

            # Calculate a self._lineHeight value from the leftmost image sizes.
            # May be toggle off. Then CustomTreeCtrl will spread when
            # necessary (which might look ugly).
            n = self._imageListLeft.GetImageCount()

            for i in range(n):

                width, height = self._imageListLeft.GetSize(i)

                if height > self._lineHeight:
                    self._lineHeight = height

        if self._lineHeight < 30:
            self._lineHeight += 2                 # at least 2 pixels
        else:
            self._lineHeight += self._lineHeight//10   # otherwise 10% extra spacing


    def SetImageList(self, imageList):
        """
        Sets the normal image list for :class:`CustomTreeCtrl`.

        :param `imageList`: an instance of :class:`wx.ImageList`.
        """

        if self._ownsImageListNormal:
            del self._imageListNormal

        self._imageListNormal = imageList
        self._ownsImageListNormal = False
        self._dirty = True

        # Don't do any drawing if we're setting the list to NULL,
        # since we may be in the process of deleting the tree control.
        if imageList:
            self.CalculateLineHeight()

            # We gray out the image list to use the grayed icons with disabled items
            sz = imageList.GetSize(0)
            self._grayedImageList = wx.ImageList(sz[0], sz[1], True, 0)

            for ii in range(imageList.GetImageCount()):
                bmp = imageList.GetBitmap(ii)
                newbmp = MakeDisabledBitmap(bmp)
                self._grayedImageList.Add(newbmp)


    def SetLeftImageList(self, imageList):
        """
        Sets the image list for :class:`CustomTreeCtrl` filled with images to be used on
        the leftmost part of the client area. Any item can have a leftmost image associated
        with it.

        :param `imageList`: an instance of :class:`wx.ImageList`.
        """

        self._imageListLeft = imageList
        self._ownsImageListLeft = False
        self._dirty = True

        # Don't do any drawing if we're setting the list to NULL,
        # since we may be in the process of deleting the tree control.
        if imageList:
            self.CalculateLineHeight()

            # We gray out the image list to use the grayed icons with disabled items
            sz = imageList.GetSize(0)
            self._grayedImageListLeft = wx.ImageList(sz[0], sz[1], True, 0)

            for ii in range(imageList.GetImageCount()):
                bmp = imageList.GetBitmap(ii)
                newbmp = MakeDisabledBitmap(bmp)
                self._grayedImageListLeft.Add(newbmp)


    def SetStateImageList(self, imageList):
        """
        Sets the state image list for :class:`CustomTreeCtrl` (from which application-defined
        state images are taken).

        :param `imageList`: an instance of :class:`wx.ImageList`.
        """

        if self._ownsImageListState:
            del self._imageListState

        self._imageListState = imageList
        self._ownsImageListState = False


    def SetButtonsImageList(self, imageList):
        """
        Sets the buttons image list for :class:`CustomTreeCtrl` (from which application-defined
        button images are taken).

        :param `imageList`: an instance of :class:`wx.ImageList`.
        """

        if self._ownsImageListButtons:
            del self._imageListButtons

        self._imageListButtons = imageList
        self._ownsImageListButtons = False
        self._dirty = True
        self.CalculateLineHeight()


    def SetImageListCheck(self, sizex, sizey, imglist=None):
        """
        Sets the checkbox/radiobutton image list.

        :param integer `sizex`: the width of the bitmaps in the `imglist`, in pixels;
        :param integer `sizey`: the height of the bitmaps in the `imglist`, in pixels;
        :param `imglist`: an instance of :class:`wx.ImageList`.
        """

        # Image list to hold disabled versions of each control
        self._grayedCheckList = wx.ImageList(sizex, sizey, True, 0)

        if imglist is None:

            self._imageListCheck = wx.ImageList(sizex, sizey)

            # Get the Checkboxes
            self._imageListCheck.Add(self.GetControlBmp(checkbox=True,
                                                        checked=True,
                                                        enabled=True,
                                                        x=sizex, y=sizey))
            self._grayedCheckList.Add(self.GetControlBmp(checkbox=True,
                                                         checked=True,
                                                         enabled=False,
                                                         x=sizex, y=sizey))

            self._imageListCheck.Add(self.GetControlBmp(checkbox=True,
                                                        checked=False,
                                                        enabled=True,
                                                        x=sizex, y=sizey))
            self._grayedCheckList.Add(self.GetControlBmp(checkbox=True,
                                                         checked=False,
                                                         enabled=False,
                                                         x=sizex, y=sizey))

            self._imageListCheck.Add(self.GetControlBmp(checkbox=True,
                                                        checked=2,
                                                        enabled=True,
                                                        x=sizex, y=sizey))
            self._grayedCheckList.Add(self.GetControlBmp(checkbox=True,
                                                         checked=2,
                                                         enabled=False,
                                                         x=sizex, y=sizey))

            # Get the Radio Buttons
            self._imageListCheck.Add(self.GetControlBmp(checkbox=False,
                                                        checked=True,
                                                        enabled=True,
                                                        x=sizex, y=sizey))
            self._grayedCheckList.Add(self.GetControlBmp(checkbox=False,
                                                         checked=True,
                                                         enabled=False,
                                                         x=sizex, y=sizey))

            self._imageListCheck.Add(self.GetControlBmp(checkbox=False,
                                                        checked=False,
                                                        enabled=True,
                                                        x=sizex, y=sizey))
            self._grayedCheckList.Add(self.GetControlBmp(checkbox=False,
                                                        checked=False,
                                                        enabled=False,
                                                        x=sizex, y=sizey))

        else:

            sizex, sizey = imglist.GetSize(0)
            self._imageListCheck = imglist

            for ii in range(self._imageListCheck.GetImageCount()):

                bmp = self._imageListCheck.GetBitmap(ii)
                newbmp = MakeDisabledBitmap(bmp)
                self._grayedCheckList.Add(newbmp)

        self._dirty = True

        if imglist:
            self.CalculateLineHeight()


    def AssignImageList(self, imageList):
        """
        Assigns the normal image list.

        :param `imageList`: an instance of :class:`wx.ImageList`.
        """

        self.SetImageList(imageList)
        self._ownsImageListNormal = True


    def AssignStateImageList(self, imageList):
        """
        Assigns the state image list.

        :param `imageList`: an instance of :class:`wx.ImageList`.
        """

        self.SetStateImageList(imageList)
        self._ownsImageListState = True


    def AssignButtonsImageList(self, imageList):
        """
        Assigns the button image list.

        :param `imageList`: an instance of :class:`wx.ImageList`.
        """

        self.SetButtonsImageList(imageList)
        self._ownsImageListButtons = True


    def AssignLeftImageList(self, imageList):
        """
        Assigns the image list for :class:`CustomTreeCtrl` filled with images to be used on
        the leftmost part of the client area. Any item can have a leftmost image associated
        with it.

        :param `imageList`: an instance of :class:`wx.ImageList`.
        """

        self.SetLeftImageList(imageList)
        self._ownsImageListLeft = True


# -----------------------------------------------------------------------------
# helpers
# -----------------------------------------------------------------------------

    def AdjustMyScrollbars(self):
        """ Internal method used to adjust the :class:`ScrolledWindow` scrollbars. """

        if self._freezeCount:
            # Skip if frozen. Set dirty flag to adjust when thawed.
            self._dirty = True
            return

        if self._anchor:

            x, y = self._anchor.GetSize(0, 0, self)
            y += _PIXELS_PER_UNIT + 2 # one more scrollbar unit + 2 pixels
            x += _PIXELS_PER_UNIT + 2 # one more scrollbar unit + 2 pixels
            x_pos = self.GetScrollPos(wx.HORIZONTAL)
            y_pos = self.GetScrollPos(wx.VERTICAL)
            self.SetScrollbars(_PIXELS_PER_UNIT, _PIXELS_PER_UNIT, x//_PIXELS_PER_UNIT, y//_PIXELS_PER_UNIT, x_pos, y_pos)

        else:

            self.SetScrollbars(0, 0, 0, 0)


    def GetLineHeight(self, item):
        """
        Returns the line height for the given item.

        :param `item`: an instance of :class:`GenericTreeItem`.

        :return: the item height, in pixels.
        """

        if self.GetAGWWindowStyleFlag() & TR_HAS_VARIABLE_ROW_HEIGHT:
            return int(item.GetHeight())
        else:
            return int(self._lineHeight)


    def DrawVerticalGradient(self, dc, rect, hasfocus):
        """
        Gradient fill from colour 1 to colour 2 from top to bottom.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the rectangle to be filled with the gradient shading;
        :param bool `hasfocus`: ``True`` if the main :class:`CustomTreeCtrl` has focus, ``False``
         otherwise.
        """

        oldpen = dc.GetPen()
        oldbrush = dc.GetBrush()
        dc.SetPen(wx.TRANSPARENT_PEN)

        # calculate gradient coefficients
        if hasfocus:
            col2 = self._secondcolour
            col1 = self._firstcolour
        else:
            col2 = self._hilightUnfocusedBrush.GetColour()
            col1 = self._hilightUnfocusedBrush2.GetColour()

        r1, g1, b1 = int(col1.Red()), int(col1.Green()), int(col1.Blue())
        r2, g2, b2 = int(col2.Red()), int(col2.Green()), int(col2.Blue())

        flrect = float(rect.height)

        rstep = float((r2 - r1)) / flrect
        gstep = float((g2 - g1)) / flrect
        bstep = float((b2 - b1)) / flrect

        rf, gf, bf = 0, 0, 0

        for y in range(rect.y, rect.y + rect.height):
            currCol = (int(r1 + rf), int(g1 + gf), int(b1 + bf))
            dc.SetBrush(wx.Brush(currCol, wx.BRUSHSTYLE_SOLID))
            dc.DrawRectangle(rect.x, y, rect.width, 1)
            rf = rf + rstep
            gf = gf + gstep
            bf = bf + bstep

        dc.SetPen(oldpen)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(rect)
        dc.SetBrush(oldbrush)


    def DrawHorizontalGradient(self, dc, rect, hasfocus):
        """
        Gradient fill from colour 1 to colour 2 from left to right.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the rectangle to be filled with the gradient shading;
        :param bool `hasfocus`: ``True`` if the main :class:`CustomTreeCtrl` has focus, ``False``
         otherwise.
        """

        oldpen = dc.GetPen()
        oldbrush = dc.GetBrush()
        dc.SetPen(wx.TRANSPARENT_PEN)

        # calculate gradient coefficients

        if hasfocus:
            col2 = self._secondcolour
            col1 = self._firstcolour
        else:
            col2 = self._hilightUnfocusedBrush.GetColour()
            col1 = self._hilightUnfocusedBrush2.GetColour()

        r1, g1, b1 = int(col1.Red()), int(col1.Green()), int(col1.Blue())
        r2, g2, b2 = int(col2.Red()), int(col2.Green()), int(col2.Blue())

        flrect = float(rect.width)

        rstep = float((r2 - r1)) / flrect
        gstep = float((g2 - g1)) / flrect
        bstep = float((b2 - b1)) / flrect

        rf, gf, bf = 0, 0, 0

        for x in range(rect.x, rect.x + rect.width):
            currCol = (int(r1 + rf), int(g1 + gf), int(b1 + bf))
            dc.SetBrush(wx.Brush(currCol, wx.BRUSHSTYLE_SOLID))
            dc.DrawRectangle(x, rect.y, 1, rect.height)
            rf = rf + rstep
            gf = gf + gstep
            bf = bf + bstep

        dc.SetPen(oldpen)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(rect)
        dc.SetBrush(oldbrush)


    def DrawVistaRectangle(self, dc, rect, hasfocus):
        """
        Draws the selected item(s) with the Windows Vista style.

        :param `dc`: an instance of :class:`wx.DC`;
        :param wx.Rect `rect`: the rectangle to be filled with the gradient shading;
        :param bool `hasfocus`: ``True`` if the main :class:`CustomTreeCtrl` has focus, ``False``
         otherwise.
        """

        if hasfocus:

            outer = _rgbSelectOuter
            inner = _rgbSelectInner
            top = _rgbSelectTop
            bottom = _rgbSelectBottom

        else:

            outer = _rgbNoFocusOuter
            inner = _rgbNoFocusInner
            top = _rgbNoFocusTop
            bottom = _rgbNoFocusBottom

        oldpen = dc.GetPen()
        oldbrush = dc.GetBrush()

        bdrRect = wx.Rect(*rect.Get())
        filRect = wx.Rect(*rect.Get())
        filRect.Deflate(1,1)

        r1, g1, b1 = int(top.Red()), int(top.Green()), int(top.Blue())
        r2, g2, b2 = int(bottom.Red()), int(bottom.Green()), int(bottom.Blue())

        flrect = float(filRect.height)
        if flrect < 1:
            flrect = self._lineHeight

        rstep = float((r2 - r1)) / flrect
        gstep = float((g2 - g1)) / flrect
        bstep = float((b2 - b1)) / flrect

        rf, gf, bf = 0, 0, 0
        dc.SetPen(wx.TRANSPARENT_PEN)

        for y in range(filRect.y, filRect.y + filRect.height):
            currCol = (int(r1 + rf), int(g1 + gf), int(b1 + bf))
            dc.SetBrush(wx.Brush(currCol, wx.BRUSHSTYLE_SOLID))
            dc.DrawRectangle(filRect.x, y, filRect.width, 1)
            rf = rf + rstep
            gf = gf + gstep
            bf = bf + bstep

        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.Pen(outer))
        dc.DrawRoundedRectangle(bdrRect, 3)
        bdrRect.Deflate(1, 1)
        dc.SetPen(wx.Pen(inner))
        dc.DrawRoundedRectangle(bdrRect, 2)

        dc.SetPen(oldpen)
        dc.SetBrush(oldbrush)


    def PaintItem(self, item, dc, level, align):
        """
        Actually draws an item.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param `dc`: an instance of :class:`wx.DC`;
        :param integer `level`: the item level in the tree hierarchy;
        :param integer `align`: an integer specifying the alignment type:

         =============== =========================================
         `align` Value   Description
         =============== =========================================
                0        No horizontal alignment of windows (in items with windows).
                1        Windows (in items with windows) are aligned at the same horizontal position.
                2        Windows (in items with windows) are aligned at the rightmost edge of :class:`CustomTreeCtrl`.
         =============== =========================================
        """

        attr = item.GetAttributes()

        if attr and attr.HasFont():
            dc.SetFont(attr.GetFont())
        else:
            if item.IsBold():
                dc.SetFont(self._boldFont)
            elif item.IsItalic():
                dc.SetFont(self._italicFont)
        if item.IsHyperText():
            dc.SetFont(self.GetHyperTextFont())
            if item.GetVisited():
                dc.SetTextForeground(self.GetHyperTextVisitedColour())
            else:
                dc.SetTextForeground(self.GetHyperTextNewColour())

        text_w, text_h, dummy = dc.GetFullMultiLineTextExtent(item.GetText())
        w, h = self.GetClientSize()

        image = item.GetCurrentImage()
        checkimage = item.GetCurrentCheckedImage()
        leftimage = _NO_IMAGE
        separator = item.IsSeparator()

        if self._imageListLeft:
            leftimage = item.GetLeftImage()

        image_w, image_h = 0, 0

        if image != _NO_IMAGE:

            if self._imageListNormal:

                image_w, image_h = self._imageListNormal.GetSize(image)
                image_w += 4

            else:

                image = _NO_IMAGE

        if item.GetType() != 0:
            wcheck, hcheck = self._imageListCheck.GetSize(item.GetType())
            wcheck += 4
        else:
            wcheck, hcheck = 0, 0

        if leftimage != _NO_IMAGE:
            l_image_w, l_image_h = self._imageListLeft.GetSize(leftimage)

        total_h = self.GetLineHeight(item)
        drawItemBackground = False

        if item.IsSelected():

            # under mac selections are only a rectangle in case they don't have the focus
            if wx.Platform == "__WXMAC__":
                if not self._hasFocus:
                    dc.SetBrush(wx.TRANSPARENT_BRUSH)
                    dc.SetPen(wx.Pen(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT), 1, wx.PENSTYLE_SOLID))
                else:
                    dc.SetBrush(self._hilightBrush)
            else:
                    dc.SetBrush((self._hasFocus and [self._hilightBrush] or [self._hilightUnfocusedBrush])[0])
                    drawItemBackground = True
        else:
            if attr and attr.HasBackgroundColour():
                drawItemBackground = True
                colBg = attr.GetBackgroundColour()
            else:
                colBg = self._backgroundColour

            dc.SetBrush(wx.Brush(colBg, wx.BRUSHSTYLE_SOLID))
            if attr and attr.HasBorderColour():
                colBorder = attr.GetBorderColour()
                dc.SetPen(wx.Pen(colBorder, 1))
            else:
                dc.SetPen(wx.TRANSPARENT_PEN)

        offset = (self.HasAGWFlag(TR_ROW_LINES) and [1] or [0])[0]

        if self.HasAGWFlag(TR_FULL_ROW_HIGHLIGHT):
            x = 0

            itemrect = wx.Rect(x, item.GetY()+offset, w, total_h-offset)

            if item.IsSelected():
                if self._usegradients:
                    if self._gradientstyle == 0:   # Horizontal
                        self.DrawHorizontalGradient(dc, itemrect, self._hasFocus)
                    else:                          # Vertical
                        self.DrawVerticalGradient(dc, itemrect, self._hasFocus)
                elif self._vistaselection:
                    self.DrawVistaRectangle(dc, itemrect, self._hasFocus)
                else:
                    if wx.Platform in ["__WXGTK2__", "__WXMAC__"]:
                        flags = wx.CONTROL_SELECTED
                        if self._hasFocus: flags = flags | wx.CONTROL_FOCUSED
                        wx.RendererNative.Get().DrawItemSelectionRect(self, dc, itemrect, flags)
                    else:
                        dc.DrawRectangle(itemrect)
            else:
               if drawItemBackground:
                   minusicon = wcheck + image_w - 2
                   itemrect = wx.Rect(item.GetX()+minusicon,
                                      item.GetY()+offset,
                                      item.GetWidth()-minusicon,
                                      total_h-offset)
                   dc.DrawRectangle(itemrect)

        else:

            if item.IsSelected():

                # If it's selected, and there's an image, then we should
                # take care to leave the area under the image painted in the
                # background colour.

                wnd = item.GetWindow()
                wndx = 0
                if wnd:
                    wndx, wndy = item.GetWindowSize()

                if separator:
                    item_width = w
                else:
                    item_width = item.GetWidth() - image_w - wcheck + 2 - wndx

                itemrect = wx.Rect(item.GetX() + wcheck + image_w - 2,
                                   item.GetY()+offset,
                                   item_width,
                                   total_h-offset)

                if self._usegradients:
                    if self._gradientstyle == 0:   # Horizontal
                        self.DrawHorizontalGradient(dc, itemrect, self._hasFocus)
                    else:                          # Vertical
                        self.DrawVerticalGradient(dc, itemrect, self._hasFocus)
                elif self._vistaselection:
                    self.DrawVistaRectangle(dc, itemrect, self._hasFocus)
                else:
                    if wx.Platform in ["__WXGTK2__", "__WXMAC__"]:
                        flags = wx.CONTROL_SELECTED
                        if self._hasFocus: flags = flags | wx.CONTROL_FOCUSED
                        wx.RendererNative.Get().DrawItemSelectionRect(self, dc, itemrect, flags)
                    else:
                        dc.DrawRectangle(itemrect)

            # On GTK+ 2, drawing a 'normal' background is wrong for themes that
            # don't allow backgrounds to be customized. Not drawing the background,
            # except for custom item backgrounds, works for both kinds of theme.
            elif drawItemBackground:

                minusicon = wcheck + image_w - 2

                if separator:
                    item_width = w
                else:
                    item_width = item.GetWidth()-minusicon

                itemrect = wx.Rect(item.GetX()+minusicon,
                                   item.GetY()+offset,
                                   item_width,
                                   total_h-offset)

                if self._usegradients and self._hasFocus:
                    if self._gradientstyle == 0:   # Horizontal
                        self.DrawHorizontalGradient(dc, itemrect, self._hasFocus)
                    else:                          # Vertical
                        self.DrawVerticalGradient(dc, itemrect, self._hasFocus)
                else:
                    dc.DrawRectangle(itemrect)

        if image != _NO_IMAGE:

            dc.SetClippingRegion(item.GetX(), item.GetY(), wcheck+image_w-2, total_h)
            if item.IsEnabled():
                imglist = self._imageListNormal
            else:
                imglist = self._grayedImageList

            imglist.Draw(image, dc,
                         item.GetX() + wcheck,
                         item.GetY() + ((total_h > image_h) and [(total_h-image_h)//2] or [0])[0],
                         wx.IMAGELIST_DRAW_TRANSPARENT)

            dc.DestroyClippingRegion()

        if wcheck:
            if item.IsEnabled():
                imglist = self._imageListCheck
            else:
                imglist = self._grayedCheckList

            imglist.Draw(checkimage, dc,
                         item.GetX(),
                         item.GetY() + ((total_h > hcheck) and [(total_h-hcheck)//2] or [0])[0],
                         wx.IMAGELIST_DRAW_TRANSPARENT)

        if leftimage != _NO_IMAGE:
            if item.IsEnabled():
                imglist = self._imageListLeft
            else:
                imglist = self._grayedImageListLeft

            imglist.Draw(leftimage, dc,
                         4,
                         item.GetY() + ((total_h > l_image_h) and [(total_h-l_image_h)//2] or [0])[0],
                         wx.IMAGELIST_DRAW_TRANSPARENT)

        dc.SetBackgroundMode(wx.TRANSPARENT)
        extraH = ((total_h > text_h) and [(total_h - text_h)//2] or [0])[0]

        textrect = wx.Rect(wcheck + image_w + item.GetX(), item.GetY() + extraH, text_w, text_h)

        itemText = item.GetText()
        if self.HasAGWFlag(TR_ELLIPSIZE_LONG_ITEMS) and not separator:
            xa, ya = self.CalcScrolledPosition((0, item.GetY()))
            maxsize = w - (wcheck + image_w + item.GetX()) + xa
            itemText = ChopText(dc, itemText, maxsize)

        if not item.IsEnabled():
            foreground = dc.GetTextForeground()
            dc.SetTextForeground(self._disabledColour)
            dc.DrawLabel(itemText, textrect)
            dc.SetTextForeground(foreground)
        else:
            if wx.Platform == "__WXMAC__" and item.IsSelected() and self._hasFocus:
                dc.SetTextForeground(wx.WHITE)
            dc.DrawLabel(itemText, textrect)

        wnd = item.GetWindow()
        on_right = item._windowontheright  # Helio: Should I make a getter?
        if wnd:
            if on_right:  # Helio: Original behaviour
                wndx = wcheck + image_w + item.GetX() + text_w + 4
            else:
                wndx = wcheck + item.GetX()
            xa, ya = self.CalcScrolledPosition((0, item.GetY()))
            wndx += xa
            if item.GetHeight() > item.GetWindowSize()[1]:
                ya += (item.GetHeight() - item.GetWindowSize()[1])//2

            if align == 1:
                # Horizontal alignment of windows
                if level in self.absoluteWindows:
                    wndx = self.absoluteWindows[level] + item.GetX() + 2 + xa

            elif align == 2:
                # Rightmost alignment of windows
                wndx = w - item.GetWindowSize().x - 2 + xa

            if wnd.GetPosition() != (wndx, ya):
                wnd.Move(wndx, ya, flags=wx.SIZE_ALLOW_MINUS_ONE)
            # Force window visible after any position changes were made.
            if not wnd.IsShown():
                wnd.Show()

        if separator:
            oldPen = dc.GetPen()

            if item.IsEnabled():
                if attr and attr.HasTextColour():
                    separatorPen = wx.Pen(attr.GetTextColour(), 1)
                else:
                    separatorPen = self._separatorPen
            else:
                separatorPen = wx.GREY_PEN

            dc.SetPen(separatorPen)
            dc.DrawLine(item.GetX()+2, item.GetY()+total_h//2, w, item.GetY()+total_h//2)
            dc.SetPen(oldPen)

        # restore normal font
        dc.SetFont(self._normalFont)


    # Now y stands for the top of the item, whereas it used to stand for middle !
    def PaintLevel(self, item, dc, level, y, align):
        """
        Paint a level in the hierarchy of :class:`CustomTreeCtrl`.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param `dc`: an instance of :class:`wx.DC`;
        :param integer `level`: the item level in the tree hierarchy;
        :param integer `y`: the current vertical position in the :class:`ScrolledWindow`;
        :param integer `align`: an integer specifying the alignment type:

         =============== =========================================
         `align` Value   Description
         =============== =========================================
                0        No horizontal alignment of windows (in items with windows).
                1        Windows (in items with windows) are aligned at the same horizontal position.
                2        Windows (in items with windows) are aligned at the rightmost edge of :class:`CustomTreeCtrl`.
         =============== =========================================

        """
        # Don't paint hidden items.
        if item.IsHidden():
            return y

        x = level*self._indent

        left_image_list = 0
        if self._imageListLeft:
            left_image_list += self._imageListLeft.GetBitmap(0).GetWidth()

        x += left_image_list

        if not self.HasAGWFlag(TR_HIDE_ROOT):

            x += self._indent

        elif level == 0:

            # always expand hidden root
            origY = y
            children = item.GetChildren()
            count = len(children)

            if count > 0:
                n = 0
                while n < count:
                    oldY = y
                    y = self.PaintLevel(children[n], dc, 1, y, align)
                    n = n + 1

                if not self.HasAGWFlag(TR_NO_LINES) and self.HasAGWFlag(TR_LINES_AT_ROOT) and count > 0:

                    # draw line down to last child
                    origY += self.GetLineHeight(children[0])>>1
                    oldY += self.GetLineHeight(children[n-1])>>1
                    oldPen = dc.GetPen()
                    dc.SetPen(self._dottedPen)
                    dc.DrawLine(3, origY, 3, oldY)
                    dc.SetPen(oldPen)

            return y

        item.SetX(x+self._spacing)
        item.SetY(y)

        h = self.GetLineHeight(item)
        y_top = y
        y_mid = y_top + (h>>1)
        y += h

        exposed_x = dc.LogicalToDeviceX(0)
        exposed_y = dc.LogicalToDeviceY(y_top)

        if self.IsExposed(exposed_x, exposed_y, 10000, h):  # 10000 = very much
            if wx.Platform == "__WXMAC__":
                # don't draw rect outline if we already have the
                # background colour under Mac
                pen = ((item.IsSelected() and self._hasFocus) and [self._borderPen] or [wx.TRANSPARENT_PEN])[0]
            else:
                pen = self._borderPen

            if item.IsSelected():
                if (wx.Platform == "__WXMAC__" and self._hasFocus):
                    colText = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
                else:
                    colText = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)

                if self._vistaselection:
                    colText = wx.BLACK
                    attr = item.GetAttributes()

                    if attr and attr.HasTextColour():
                        colText = attr.GetTextColour()

            else:
                attr = item.GetAttributes()
                if attr and attr.HasTextColour():
                    colText = attr.GetTextColour()
                else:
                    colText = self.GetForegroundColour()

            # prepare to draw
            dc.SetTextForeground(colText)
            dc.SetPen(pen)
            oldpen = pen

            # draw
            self.PaintItem(item, dc, level, align)

            if self.HasAGWFlag(TR_ROW_LINES):

                # if the background colour is white, choose a
                # contrasting colour for the lines
                medium_grey = wx.Pen(wx.Colour(200, 200, 200))
                dc.SetPen(((self.GetBackgroundColour() == wx.WHITE) and [medium_grey] or [wx.WHITE_PEN])[0])
                dc.DrawLine(0, y_top, 10000, y_top)
                dc.DrawLine(0, y, 10000, y)

            # restore DC objects
            dc.SetBrush(wx.WHITE_BRUSH)
            dc.SetTextForeground(wx.BLACK)

            if not self.HasAGWFlag(TR_NO_LINES):

                # draw the horizontal line here
                dc.SetPen(self._dottedPen)
                x_start = x
                if x > self._indent+left_image_list:
                    x_start -= self._indent
                elif self.HasAGWFlag(TR_LINES_AT_ROOT):
                    x_start = 3
                dc.DrawLine(x_start, y_mid, x + self._spacing, y_mid)
                dc.SetPen(oldpen)

            # should the item show a button?
            if item.HasPlus() and self.HasButtons():

                if self._imageListButtons:

                    # draw the image button here
                    image_h = 0
                    image_w = 0
                    image = (item.IsExpanded() and [TreeItemIcon_Expanded] or [TreeItemIcon_Normal])[0]
                    if item.IsSelected():
                        image += TreeItemIcon_Selected - TreeItemIcon_Normal

                    image_w, image_h = self._imageListButtons.GetSize(image)
                    xx = x - image_w//2
                    yy = y_mid - image_h//2

                    dc.SetClippingRegion(xx, yy, image_w, image_h)
                    self._imageListButtons.Draw(image, dc, xx, yy,
                                                wx.IMAGELIST_DRAW_TRANSPARENT)
                    dc.DestroyClippingRegion()

                else: # no custom buttons

                    if self.HasAGWFlag(TR_TWIST_BUTTONS):
                        # We draw something like the Mac twist buttons

                        dc.SetPen(wx.BLACK_PEN)
                        dc.SetBrush(self._hilightBrush)
                        button = [wx.Point(), wx.Point(), wx.Point()]

                        if item.IsExpanded():
                            button[0].x = x - 5
                            button[0].y = y_mid - 3
                            button[1].x = x + 5
                            button[1].y = button[0].y
                            button[2].x = x
                            button[2].y = button[0].y + 6
                        else:
                            button[0].x = x - 3
                            button[0].y = y_mid - 5
                            button[1].x = button[0].x
                            button[1].y = y_mid + 5
                            button[2].x = button[0].x + 5
                            button[2].y = y_mid

                        dc.DrawPolygon(button)

                    else:
                        # These are the standard wx.TreeCtrl buttons as wx.RendererNative knows

                        wImage = 11
                        hImage = 11

                        flag = 0

                        if item.IsExpanded():
                            flag |= _CONTROL_EXPANDED
                        if item == self._underMouse:
                            flag |= _CONTROL_CURRENT

                        self._drawingfunction(self, dc, wx.Rect(x - wImage//2, y_mid - hImage//2, wImage, hImage), flag)

        if item.IsExpanded():

            children = item.GetChildren()
            count = len(children)

            if count > 0:

                n = 0
                level = level + 1

                while n < count:
                    oldY = y
                    y = self.PaintLevel(children[n], dc, level, y, align)
                    n = n + 1

                if not self.HasAGWFlag(TR_NO_LINES) and count > 0:

                    # draw line down to last child
                    oldY += self.GetLineHeight(children[n-1])>>1
                    if self.HasButtons():
                        y_mid += 5

                    # Only draw the portion of the line that is visible, in case it is huge
                    xOrigin, yOrigin = dc.GetDeviceOrigin()
                    yOrigin = abs(yOrigin)
                    width, height = self.GetClientSize()

                    # Move end points to the beginning/end of the view?
                    if y_mid < yOrigin:
                        y_mid = yOrigin
                    if oldY > yOrigin + height:
                        oldY = yOrigin + height

                    # after the adjustments if y_mid is larger than oldY then the line
                    # isn't visible at all so don't draw anything
                    if y_mid < oldY:
                        dc.SetPen(self._dottedPen)
                        dc.DrawLine(x, y_mid, x, oldY)

        return y


# -----------------------------------------------------------------------------
# wxWidgets callbacks
# -----------------------------------------------------------------------------

    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`CustomTreeCtrl`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """

        dc = wx.PaintDC(self)
        self.PrepareDC(dc)

        if not self._anchor:
            return

        dc.SetFont(self._normalFont)
        dc.SetPen(self._dottedPen)

        align = 0

        if self.HasAGWFlag(TR_ALIGN_WINDOWS):
            align = 1
        elif self.HasAGWFlag(TR_ALIGN_WINDOWS_RIGHT):
            align = 2

        y = 2
        self.PaintLevel(self._anchor, dc, 0, y, align)


    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`CustomTreeCtrl`.

        :param `event`: a :class:`wx.SizeEvent` event to be processed.
        """

        if self.HasAGWFlag(TR_ELLIPSIZE_LONG_ITEMS):
            self.Refresh()
            event.Skip()
            return

        if self.HasAGWFlag(TR_ALIGN_WINDOWS_RIGHT) and self._itemWithWindow:
            self.RefreshItemWithWindows()
        else:
            self.RefreshSelected()

        event.Skip()


    def OnEraseBackground(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for :class:`CustomTreeCtrl`.

        :param `event`: a :class:`EraseEvent` event to be processed.
        """

        # Can we actually do something here (or in OnPaint()) To Handle
        # background images that are stretchable or always centered?
        # I tried but I get enormous flickering...

        if not self._backgroundImage:
            event.Skip()
            return

        if self._imageStretchStyle == _StyleTile:
            dc = event.GetDC()

            if not dc:
                dc = wx.ClientDC(self)
                rect = self.GetUpdateRegion().GetBox()
                dc.SetClippingRegion(rect)

            self.TileBackground(dc)


    def TileBackground(self, dc):
        """
        Tiles the background image to fill all the available area.

        :param `dc`: an instance of :class:`wx.DC`.

        .. todo:: Support background images also in stretch and centered modes.
        """

        sz = self.GetClientSize()
        w = self._backgroundImage.GetWidth()
        h = self._backgroundImage.GetHeight()

        x = 0

        while x < sz.width:
            y = 0

            while y < sz.height:
                dc.DrawBitmap(self._backgroundImage, x, y, True)
                y = y + h

            x = x + w


    def OnSetFocus(self, event):
        """
        Handles the ``wx.EVT_SET_FOCUS`` event for :class:`CustomTreeCtrl`.

        :param `event`: a :class:`FocusEvent` event to be processed.
        """

        self._hasFocus = True
        self.RefreshSelected()
        event.Skip()


    def OnKillFocus(self, event):
        """
        Handles the ``wx.EVT_KILL_FOCUS`` event for :class:`CustomTreeCtrl`.

        :param `event`: a :class:`FocusEvent` event to be processed.
        """

        self._hasFocus = False
        self.RefreshSelected()
        event.Skip()


    def OnKeyDown(self, event):
        """
        Handles the ``wx.EVT_KEY_DOWN`` event for :class:`CustomTreeCtrl`, sending a
        ``EVT_TREE_KEY_DOWN`` event.

        :param `event`: a :class:`KeyEvent` event to be processed.
        """

        te = TreeEvent(wxEVT_TREE_KEY_DOWN, self.GetId())
        te._evtKey = event
        te.SetEventObject(self)

        if self.GetEventHandler().ProcessEvent(te):
            # intercepted by the user code
            return

        if self._current is None or self._key_current is None:

            self._current = self._key_current = self.GetFirstVisibleItem()

        # how should the selection work for this event?
        is_multiple, extended_select, unselect_others = EventFlagsToSelType(self.GetAGWWindowStyleFlag(),
                                                                            event.ShiftDown(), event.CmdDown())

        # + : Expand
        # - : Collaspe
        # * : Expand all/Collapse all
        # ' ' | return : activate
        # up    : go up (not last children!)
        # down  : go down
        # left  : go to parent
        # right : open if parent and go next
        # home  : go to root
        # end   : go to last item without opening parents
        # alnum : start or continue searching for the item with this prefix

        keyCode = event.GetKeyCode()

        if keyCode in (ord('+'), wx.WXK_ADD, wx.WXK_NUMPAD_ADD):				# "+"
            if self._current.HasPlus() and not self.IsExpanded(self._current) and self.IsItemEnabled(self._current):
                self.Expand(self._current)

        elif keyCode in (ord('*'), wx.WXK_MULTIPLY, wx.WXK_NUMPAD_MULTIPLY):	# "*"
            if not self.IsExpanded(self._current) and self.IsItemEnabled(self._current):
                # expand all
                self.ExpandAllChildren(self._current)

        elif keyCode in (ord('-'), wx.WXK_SUBTRACT, wx.WXK_NUMPAD_SUBTRACT):	# "-"
            if self.IsExpanded(self._current):
                self.Collapse(self._current)

        elif keyCode in (wx.WXK_MENU, wx.WXK_WINDOWS_MENU):
            # Use the item's bounding rectangle to determine position for the event
            itemRect = self.GetBoundingRect(self._current, True)
            event = TreeEvent(wxEVT_TREE_ITEM_MENU, self.GetId())
            event._item = self._current
            # Use the left edge, vertical middle
            event._pointDrag = wx.Point(itemRect.GetX(), itemRect.GetY() + itemRect.GetHeight()//2)
            event.SetEventObject(self)
            self.GetEventHandler().ProcessEvent(event)

        elif keyCode in (wx.WXK_RETURN, wx.WXK_SPACE, wx.WXK_NUMPAD_ENTER):

            if not self._current or not self.IsItemEnabled(self._current):
                event.Skip()
                return

            if not event.HasModifiers():
                event = TreeEvent(wxEVT_TREE_ITEM_ACTIVATED, self.GetId())
                event._item = self._current
                event.SetEventObject(self)
                self.GetEventHandler().ProcessEvent(event)

                if keyCode == wx.WXK_SPACE and self.GetItemType(self._current) > 0:
                    if self.IsItem3State(self._current):
                        checked = self.GetItem3StateValue(self._current)
                        checked = (checked+1)%3
                    else:
                        checked = not self.IsItemChecked(self._current)

                    self.CheckItem(self._current, checked)

                if self.IsItemHyperText(self._current):
                    self.HandleHyperLink(self._current)

            # in any case, also generate the normal key event for this key,
            # even if we generated the ACTIVATED event above: this is what
            # wxMSW does and it makes sense because you might not want to
            # process ACTIVATED event at all and handle Space and Return
            # directly (and differently) which would be impossible otherwise
            event.Skip()

        # up goes to the previous sibling or to the last
        # of its children if it's expanded
        elif keyCode == wx.WXK_UP:
            # Search for a previous, enabled item.
            prev = self.GetPrevShown(self._key_current)
            while prev and self.IsItemEnabled(prev) is False:
                prev = self.GetPrevShown(prev)

            # If we found a valid enabled item, select it.
            if prev:
                self.DoSelectItem(prev, unselect_others, extended_select, from_key=True)
                self._key_current = prev

        # left arrow goes to the parent
        elif keyCode == wx.WXK_LEFT:

            prev = self.GetItemParent(self._current)
            if prev == self.GetRootItem() and self.HasAGWFlag(TR_HIDE_ROOT):
                # don't go to root if it is hidden
                prev = self.GetPrevSibling(self._current)

            if self.IsExpanded(self._current):
                self.Collapse(self._current)
            else:
                if prev and self.IsItemEnabled(prev):
                    self.DoSelectItem(prev, unselect_others, extended_select, from_key=True)

        elif keyCode == wx.WXK_RIGHT:
            # this works the same as the down arrow except that we
            # also expand the item if it wasn't expanded yet
            if self.IsExpanded(self._current) and self.HasChildren(self._current):
                child, cookie = self.GetFirstChild(self._key_current)
                if self.IsItemEnabled(child):
                    self.DoSelectItem(child, unselect_others, extended_select, from_key=True)
                    self._key_current = child
            else:
                self.Expand(self._current)
            # fall through

        elif keyCode == wx.WXK_DOWN:

            # Scan for next enabled item.
            next = self.GetNextShown(self._key_current)
            while next and self.IsItemEnabled(next) is False:
                next = self.GetNextShown(next)

            if next:
                self.DoSelectItem(next, unselect_others, extended_select, from_key=True)
                self._key_current = next

        # <End> selects the last enabled tree item.
        elif keyCode == wx.WXK_END:

            top = self.GetRootItem()
            if self.HasAGWFlag(TR_HIDE_ROOT):
                top, cookie = self.GetFirstChild(top)

            lastEnabled = None
            while top:
                # Keep track of last enabled item encountered.
                if self.IsItemEnabled(top):
                    lastEnabled = top
                # Top-most item is not enabled. Scan for next item.
                top = self.GetNextShown(top)

            if lastEnabled:
                self.DoSelectItem(lastEnabled, unselect_others, extended_select, from_key=True)

        # <Home> selects the first enabled tree item.
        elif keyCode == wx.WXK_HOME:

            top = self.GetRootItem()
            if self.HasAGWFlag(TR_HIDE_ROOT):
                top, cookie = self.GetFirstChild(top)

            # Scan for first enabled and displayed item.
            while top and self.IsItemEnabled(top) is False:
                top = self.GetNextShown(top)

            if top:
                self.DoSelectItem(top, unselect_others, extended_select, from_key=True)

        # <PgUp> moves up by a page
        elif keyCode in (wx.WXK_PAGEUP, wx.WXK_NUMPAD_PAGEUP):
            # Get Current tree Item.
            currentItem = self.GetSelection()
            if not currentItem:
                # Nothing selected. Allow normal ScrolledWindow PageUp handling.
                event.Skip()
                return
            # Is the current item visible?
            clientWidth, clientHeight = self.GetClientSize()
            itemHeight = currentItem.GetHeight()
            pageSize = max(int(clientHeight * 0.9), clientHeight - itemHeight)
            x, y = self.CalcScrolledPosition(0, currentItem.GetY())
            if y >= 0 and (y + itemHeight) < clientHeight:
                visCount = 1    # Current item is visible
            else:
                visCount = 0    # Current item not visible.
            # Move upwards in tree until last visible, or pagesize hit.
            amount = 0
            targetItem = currentItem
            prevItem = self.GetPrevShown(currentItem)
            while prevItem:
                itemHeight = prevItem.GetHeight()
                if visCount:
                    # Is this item also visible?
                    x, y = self.CalcScrolledPosition(0, prevItem.GetY())
                    if y >= 0 and (y + itemHeight) < clientHeight:
                        visCount += 1
                    else:
                        if visCount > 1 and targetItem != currentItem:
                            # Move to top visible item in page.
                            break
                        visCount = 0
                # Move up to previous item, set as target if it is enabled.
                if prevItem.IsEnabled():
                    targetItem = prevItem
                amount += itemHeight
                # Break loop if we moved up a page size and have a new target.
                if amount > pageSize and targetItem != currentItem:
                    break
                prevItem = self.GetPrevShown(prevItem)
            # If we found a valid target, select it.
            if targetItem != currentItem:
                self.DoSelectItem(targetItem, unselect_others=True,
                                  extended_select=False, from_key=True)
            else:
                # No enabled item found. Let ScrolledWindow handle PageUp.
                event.Skip()

        # <PgDn> moves down by a page
        elif keyCode in (wx.WXK_PAGEDOWN, wx.WXK_NUMPAD_PAGEDOWN):
            # Get Current tree Item.
            currentItem = self.GetSelection()
            if not currentItem:
                # Nothing selected. Allow normal ScrolledWindow PgDn handling.
                event.Skip()
                return
            # Is the current item visible?
            clientWidth, clientHeight = self.GetClientSize()
            itemHeight = currentItem.GetHeight()
            pageSize = max(int(clientHeight * 0.9), clientHeight - itemHeight)
            x, y = self.CalcScrolledPosition(0, currentItem.GetY())
            if y >= 0 and (y + itemHeight) < clientHeight:
                visCount = 1    # Current item is visible
            else:
                visCount = 0    # Current item not visible.
            # Move downwards in tree until last visible, or pagesize hit.
            amount = 0
            targetItem = currentItem
            nextItem = self.GetNextShown(currentItem)
            while nextItem:
                itemHeight = nextItem.GetHeight()
                if visCount:
                    # Is this item also visible?
                    x, y = self.CalcScrolledPosition(0, nextItem.GetY())
                    if y >= 0 and (y + itemHeight) < clientHeight:
                        visCount += 1
                    else:
                        if visCount > 1 and targetItem != currentItem:
                            # Move to last visible item in page.
                            break
                        visCount = 0
                # Move down to next item, set as target if it is enabled.
                if nextItem.IsEnabled():
                    targetItem = nextItem
                amount += itemHeight
                # Break loop if we moved down a page size and have a new target.
                if amount > pageSize and targetItem != currentItem:
                    break
                nextItem = self.GetNextShown(nextItem)
            # If we found a valid target, select it.
            if targetItem != currentItem:
                self.DoSelectItem(targetItem, unselect_others=True,
                                  extended_select=False, from_key=True)
            else:
                # No enabled item found. Let ScrolledWindow handle PageDown.
                event.Skip()

        # Some other key pressed. Consume character for item search.
        else:

            if not event.HasModifiers() and ((keyCode >= ord('0') and keyCode <= ord('9')) or \
                                             (keyCode >= ord('a') and keyCode <= ord('z')) or \
                                             (keyCode >= ord('A') and keyCode <= ord('Z'))):

                # find the next item starting with the given prefix
                ch = chr(keyCode)
                id = self.FindItem(self._current, self._findPrefix + ch)

                if not id:
                    # no such item
                    return

                if self.IsItemEnabled(id):
                    self.SelectItem(id)
                self._findPrefix += ch

                # also start the timer to reset the current prefix if the user
                # doesn't press any more alnum keys soon -- we wouldn't want
                # to use this prefix for a new item search
                if not self._findTimer:
                    self._findTimer = TreeFindTimer(self)

                self._findTimer.Start(_DELAY, wx.TIMER_ONE_SHOT)

            else:

                event.Skip()


    def GetPrevShown(self, item):
        """
        Returns the previous displayed item in the tree. This is either the
        last displayed child of its previous sibling, or its parent item.

        :param `item`: an instance of :class:`GenericTreeItem`;

        :return: An instance of :class:`GenericTreeItem` or ``None`` if no previous item found (root).
        """
        if not item:
            return None
        # Try to get previous sibling.
        prev = self.GetPrevSibling(item)
        if prev:
            # Drill down to last displayed child of previous sibling.
            while self.IsExpanded(prev) and self.HasChildren(prev):
                prev = self.GetLastChild(prev)
        else:
            # No previous sibling. Move to parent.
            prev = self.GetItemParent(item)
        # Suppress returning root item if TR_HIDE_ROOT flag is set.
        if prev == self.GetRootItem() and self.HasAGWFlag(TR_HIDE_ROOT):
            return None
        return prev


    def GetNextShown(self, item):
        """
        Returns the next displayed item in the tree. This is either the first
        child of the item (if it is expanded and has children) or its next
        sibling. If there is no next sibling the tree is walked backwards
        until a next sibling for one of its parents is found.

        :param `item`: an instance of :class:`GenericTreeItem`;

        :return: An instance of :class:`GenericTreeItem` or ``None`` if no item follows this one.
        """
        if not item:
            return None
        # Is the item expanded and has children?
        if self.IsExpanded(item) and self.HasChildren(item):
            # Next item = first child.
            next, cookie = self.GetFirstChild(item)
        else:
            # Next item = next sibling.
            sibling = self.GetNextSibling(item)
            parent = self.GetItemParent(item)
            while not sibling and parent and parent != self.GetRootItem():
                # No sibling. Try parent's sibling until root reached.
                sibling = self.GetNextSibling(parent)
                parent = self.GetItemParent(parent)
            next = sibling
        # Return the next item.
        return next


    def GetNextActiveItem(self, item, down=True):
        """
        Returns the next active item. Used Internally at present.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `down`: ``True`` to search downwards in the hierarchy for an active item,
         ``False`` to search upwards.

        :return: An instance of :class:`GenericTreeItem` if an active item has been found or
         ``None`` if none has been found.
        """

        if down:
            sibling = self.GetNextSibling
        else:
            sibling = self.GetPrevSibling

        if self.GetItemType(item) == 2 and not self.IsItemChecked(item):
            # Is an unchecked radiobutton... all its children are inactive
            # try to get the next/previous sibling
            found = 0

            while 1:
                child = sibling(item)
                if (child and self.IsItemEnabled(child)) or not child:
                    break
                item = child

        else:
            # Tha's not a radiobutton... but some of its children can be
            # inactive
            child, cookie = self.GetFirstChild(item)
            while child and not self.IsItemEnabled(child):
                child, cookie = self.GetNextChild(item, cookie)

        if child and self.IsItemEnabled(child):
            return child

        return None


    def HitTest(self, point, flags=0):
        """
        Calculates which (if any) item is under the given point, returning the tree item
        at this point plus extra information flags.

        :param `point`: an instance of :class:`wx.Point`, a point to test for hits;
        :param integer `flags`: a bitlist of the following values:

         ================================== =============== =================================
         HitTest Flags                      Hex Value       Description
         ================================== =============== =================================
         ``TREE_HITTEST_ABOVE``                         0x1 Above the client area
         ``TREE_HITTEST_BELOW``                         0x2 Below the client area
         ``TREE_HITTEST_NOWHERE``                       0x4 No item has been hit
         ``TREE_HITTEST_ONITEMBUTTON``                  0x8 On the button associated to an item
         ``TREE_HITTEST_ONITEMICON``                   0x10 On the icon associated to an item
         ``TREE_HITTEST_ONITEMINDENT``                 0x20 On the indent associated to an item
         ``TREE_HITTEST_ONITEMLABEL``                  0x40 On the label (string) associated to an item
         ``TREE_HITTEST_ONITEM``                       0x50 Anywhere on the item
         ``TREE_HITTEST_ONITEMRIGHT``                  0x80 On the right of the label associated to an item
         ``TREE_HITTEST_TOLEFT``                      0x200 On the left of the client area
         ``TREE_HITTEST_TORIGHT``                     0x400 On the right of the client area
         ``TREE_HITTEST_ONITEMUPPERPART``             0x800 On the upper part (first half) of the item
         ``TREE_HITTEST_ONITEMLOWERPART``            0x1000 On the lower part (second half) of the item
         ``TREE_HITTEST_ONITEMCHECKICON``            0x2000 On the check/radio icon, if present
         ================================== =============== =================================

        :return: A tuple with the first value being an instance of :class:`GenericTreeItem` or ``None`` if
         no item has been hit-tested, and as second value an integer parameter `flag`.

        :note: both the item (if any, ``None`` otherwise) and the `flags` are always returned as a tuple.
        """

        w, h = self.GetSize()
        flags = 0

        pointX, pointY = point[0], point[1]
        if pointX < 0:
            flags |= TREE_HITTEST_TOLEFT
        if pointX > w:
            flags |= TREE_HITTEST_TORIGHT
        if pointY < 0:
            flags |= TREE_HITTEST_ABOVE
        if pointY > h:
            flags |= TREE_HITTEST_BELOW

        if flags:
            return None, flags

        if self._anchor is None:
            flags = TREE_HITTEST_NOWHERE
            return None, flags

        point = self.CalcUnscrolledPosition(*point)
        hit, flags = self._anchor.HitTest(point, self, flags, 0)

        if hit is None:
            flags = TREE_HITTEST_NOWHERE
            return None, flags

        if not self.IsItemEnabled(hit):
            return None, flags

        return hit, flags


    def GetBoundingRect(self, item, textOnly=False):
        """
        Retrieves the rectangle bounding the item.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param bool `textOnly`: if ``True``, only the rectangle around the item's label will
         be returned, otherwise the item's image is also taken into account.

        :return: An instance of :class:`wx.Rect`.

        :note: The rectangle coordinates are logical, not physical ones. So, for example,
         the `x` coordinate may be negative if the tree has a horizontal scrollbar and its
         position is not ``0``.

        .. warning:: The ``textOnly`` flag is currently ignored and this method
         always returns the rectangle including the item's image, checkbox,
         and window (if they exist) along with the item's text. A separator's
         bounding box stretches the width of the entire client area. The height
         may be 0 for newly added items until :meth:`CustomTreeCtrl.CalculateSize`
         is called while the tree is not frozen.
        """

        i = item

        startX, startY = self.GetViewStart()
        rect = wx.Rect()

        rect.x = i.GetX() - startX*_PIXELS_PER_UNIT
        rect.y = i.GetY() - startY*_PIXELS_PER_UNIT
        rect.width = i.GetWidth()
        rect.height = self.GetLineHeight(i)

        return rect


    def Edit(self, item):
        """
        Internal function. Starts the editing of an item label, sending a
        ``EVT_TREE_BEGIN_LABEL_EDIT`` event.

        :param `item`: an instance of :class:`GenericTreeItem`.

        .. warning:: Separator-type items can not be edited.
        """

        if item.IsSeparator():
            return

        te = TreeEvent(wxEVT_TREE_BEGIN_LABEL_EDIT, self.GetId())
        te._item = item
        te.SetEventObject(self)
        if self.GetEventHandler().ProcessEvent(te) and not te.IsAllowed():
            # vetoed by user
            return

        # We have to call this here because the label in
        # question might just have been added and no screen
        # update taken place.
        if self._dirty:
            if wx.Platform in ["__WXMSW__", "__WXMAC__"]:
                self.Update()
            else:
                wx.YieldIfNeeded()

        if self._editCtrl is not None and item != self._editCtrl.item():
            self._editCtrl.StopEditing()

        if self._editCtrl is None:
            self._editCtrl = TreeTextCtrl(self, item=item)
            self._editCtrl.SetFocus()


    def GetEditControl(self):
        """
        Returns a reference to the edit :class:`TreeTextCtrl` if the item is being edited or
        ``None`` otherwise (it is assumed that no more than one item may be edited
        simultaneously).
        """

        return self._editCtrl


    def OnAcceptEdit(self, item, value):
        """
        Called by :class:`TreeTextCtrl`, to accept the changes and to send the
        ``EVT_TREE_END_LABEL_EDIT`` event.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param string `value`: the new value of the item label.

        :return: ``True`` if the editing has not been vetoed, ``False`` otherwise.
        """

        le = TreeEvent(wxEVT_TREE_END_LABEL_EDIT, self.GetId())
        le._item = item
        le.SetEventObject(self)
        le._label = value
        le._editCancelled = False

        return not self.GetEventHandler().ProcessEvent(le) or le.IsAllowed()


    def OnCancelEdit(self, item):
        """
        Called by :class:`TreeTextCtrl`, to cancel the changes and to send the
        ``EVT_TREE_END_LABEL_EDIT`` event.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        # let owner know that the edit was cancelled
        le = TreeEvent(wxEVT_TREE_END_LABEL_EDIT, self.GetId())
        le._item = item
        le.SetEventObject(self)
        le._label = ""
        le._editCancelled = True

        self.GetEventHandler().ProcessEvent(le)


    def OnEditTimer(self):
        """ The timer for editing has expired. Start editing. """

        self.Edit(self._current)


    def OnMouse(self, event):
        """
        Handles a bunch of ``wx.EVT_MOUSE_EVENTS`` events for :class:`CustomTreeCtrl`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if not self._anchor:
            return

        pt = wx.Point(self.CalcUnscrolledPosition(*event.GetPosition()))

        # Is the mouse over a tree item button?
        flags = 0
        thisItem, flags = self._anchor.HitTest(pt, self, flags, 0)
        underMouse = thisItem
        underMouseChanged = underMouse != self._underMouse

        if underMouse and (flags & TREE_HITTEST_ONITEM) and not event.LeftIsDown() and \
           not self._isDragging and (not self._editTimer or not self._editTimer.IsRunning()):
            underMouse = underMouse
        else:
            underMouse = None

        if underMouse != self._underMouse:
            if self._underMouse:
                # unhighlight old item
                self._underMouse = None

            self._underMouse = underMouse

        # Determines what item we are hovering over and need a tooltip for
        hoverItem = thisItem

        # We do not want a tooltip if we are dragging, or if the edit timer is running
        if underMouseChanged and not self._isDragging and (not self._editTimer or not self._editTimer.IsRunning()):

            if hoverItem is not None:
                # Ask the tree control what tooltip (if any) should be shown
                hevent = TreeEvent(wxEVT_TREE_ITEM_GETTOOLTIP, self.GetId())
                hevent._item = hoverItem
                hevent.SetEventObject(self)

                if self.GetEventHandler().ProcessEvent(hevent) and hevent.IsAllowed():
                    self.SetToolTip(hevent._label)

                elif self.HasAGWFlag(TR_TOOLTIP_ON_LONG_ITEMS):

                    tip = self.GetToolTipText()

                    if hoverItem.IsSeparator():
                        if tip:
                            self.SetToolTip('')
                    else:
                        maxsize = self.GetItemSize(hoverItem)
                        itemText = hoverItem.GetText()

                        dc = wx.ClientDC(self)

                        if dc.GetFullMultiLineTextExtent(itemText)[0] > maxsize:
                            if tip != itemText:
                                self.SetToolTip(itemText)
                        else:
                            if tip:
                                self.SetToolTip('')

                if hoverItem.IsHyperText() and (flags & TREE_HITTEST_ONITEMLABEL) and hoverItem.IsEnabled():
                    self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
                    self._isonhyperlink = True
                else:
                    if self._isonhyperlink:
                        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
                        self._isonhyperlink = False

        # we process left mouse up event (enables in-place edit), right down
        # (pass to the user code), left dbl click (activate item) and
        # dragging/moving events for items drag-and-drop

        if not (event.LeftDown() or event.LeftUp() or event.RightDown() or event.LeftDClick() or \
                event.Dragging() or ((event.Moving() or event.RightUp()) and self._isDragging)):

            event.Skip()
            return

        flags = 0
        item, flags = self._anchor.HitTest(pt, self, flags, 0)

        if event.Dragging() and not self._isDragging and ((flags & TREE_HITTEST_ONITEMICON) or (flags & TREE_HITTEST_ONITEMLABEL)):

            if self._dragCount == 0:
                self._dragStart = pt

            self._countDrag = 0
            self._dragCount = self._dragCount + 1

            if self._dragCount != 3:
                # wait until user drags a bit further...
                return

            command = (event.RightIsDown() and [wxEVT_TREE_BEGIN_RDRAG] or [wxEVT_TREE_BEGIN_DRAG])[0]

            nevent = TreeEvent(command, self.GetId())
            nevent._item = self._current
            nevent.SetEventObject(self)
            newpt = self.CalcScrolledPosition(*pt)
            nevent.SetPoint(newpt)

            # by default the dragging is not supported, the user code must
            # explicitly allow the event for it to take place
            nevent.Veto()

            if self.GetEventHandler().ProcessEvent(nevent) and nevent.IsAllowed():

                # we're going to drag this item
                self._isDragging = True

                # remember the old cursor because we will change it while
                # dragging
                self._oldCursor = self._cursor

                # in a single selection control, hide the selection temporarily
                if not (self.GetAGWWindowStyleFlag() & TR_MULTIPLE):
                    self._oldSelection = self.GetSelection()

                    if self._oldSelection:

                        self._oldSelection.SetHilight(False)
                        self.RefreshLine(self._oldSelection)
                else:
                    selections = self.GetSelections()
                    if len(selections) == 1:
                        self._oldSelection = selections[0]
                        self._oldSelection.SetHilight(False)
                        self.RefreshLine(self._oldSelection)

                if self._dragImage:
                    del self._dragImage

                # Create the custom draw image from the icons and the text of the item
                self._dragImage = DragImage(self, self._current)
                self._dragImage.BeginDrag(wx.Point(0,0), self, fullScreen=self._dragFullScreen)
                self._dragImage.Show()
                self._dragImage.Move(self.CalcScrolledPosition(*pt))

        elif event.Dragging() and self._isDragging:

            self._dragImage.Move(self.CalcScrolledPosition(*pt))

            if self._dragFullScreen is True:
                # Don't highlight target items if dragging full-screen.
                return

            if self._countDrag == 0 and item:
                self._oldItem = item

            if item != self._dropTarget:

                # unhighlight the previous drop target
                if self._dropTarget:
                    self._dropTarget.SetHilight(False)
                    self.RefreshLine(self._dropTarget)
                if item:
                    item.SetHilight(True)
                    self.RefreshLine(item)
                    self._countDrag = self._countDrag + 1
                self._dropTarget = item

                self.Update()

            if self._countDrag >= 3:
                # Here I am trying to avoid ugly repainting problems... hope it works
                self.RefreshLine(self._oldItem)
                self._countDrag = 0

        elif (event.LeftUp() or event.RightUp()) and self._isDragging:

            if self._dragImage:
                self._dragImage.EndDrag()

            if self._dropTarget:
                self._dropTarget.SetHilight(False)

            if self._oldSelection:

                self._oldSelection.SetHilight(True)
                self.RefreshLine(self._oldSelection)
                self._oldSelection = None

            # generate the drag end event
            event = TreeEvent(wxEVT_TREE_END_DRAG, self.GetId())
            event._item = item
            event._pointDrag = self.CalcScrolledPosition(*pt)
            event.SetEventObject(self)

            self.GetEventHandler().ProcessEvent(event)

            self._isDragging = False
            self._dropTarget = None

            self.SetCursor(self._oldCursor)

            if wx.Platform in ["__WXMSW__", "__WXMAC__"]:
                self.Refresh()
            else:
                # Probably this is not enough on GTK. Try a Refresh() if it does not work.
                wx.YieldIfNeeded()

        else:

            # If we got to this point, we are not dragging or moving the mouse.
            # Because the code in carbon/toplevel.cpp will only set focus to the tree
            # if we skip for EVT_LEFT_DOWN, we MUST skip this event here for focus to work.
            # We skip even if we didn't hit an item because we still should
            # restore focus to the tree control even if we didn't exactly hit an item.
            if event.LeftDown():
                self._hasFocus = True
                self.SetFocusIgnoringChildren()
                event.Skip()

            # here we process only the messages which happen on tree items

            self._dragCount = 0

            if item is None:
                if self._editCtrl is not None and item != self._editCtrl.item():
                    self._editCtrl.StopEditing()
                return  # we hit the blank area

            if event.RightDown():

                if self._editCtrl is not None and item != self._editCtrl.item():
                    self._editCtrl.StopEditing()

                self._hasFocus = True
                self.SetFocusIgnoringChildren()

                # If the item is already selected, do not update the selection.
                # Multi-selections should not be cleared if a selected item is clicked.
                if not self.IsSelected(item):

                    self.DoSelectItem(item, True, False)

                nevent = TreeEvent(wxEVT_TREE_ITEM_RIGHT_CLICK, self.GetId())
                nevent._item = item
                nevent._pointDrag = self.CalcScrolledPosition(*pt)
                nevent.SetEventObject(self)
                event.Skip(not self.GetEventHandler().ProcessEvent(nevent))

                # Consistent with MSW (for now), send the ITEM_MENU *after*
                # the RIGHT_CLICK event. TODO: This behaviour may change.
                nevent2 = TreeEvent(wxEVT_TREE_ITEM_MENU, self.GetId())
                nevent2._item = item
                nevent2._pointDrag = self.CalcScrolledPosition(*pt)
                nevent2.SetEventObject(self)
                self.GetEventHandler().ProcessEvent(nevent2)

            elif event.LeftUp():

                # this facilitates multiple-item drag-and-drop

                if self.HasAGWFlag(TR_MULTIPLE):

                    selections = self.GetSelections()

                    if len(selections) > 1 and not event.CmdDown() and not event.ShiftDown():

                        self.DoSelectItem(item, True, False)

                if self._lastOnSame:

                    if item == self._current and (flags & TREE_HITTEST_ONITEMLABEL) and self.HasAGWFlag(TR_EDIT_LABELS):

                        if self._editTimer:

                            if self._editTimer.IsRunning():

                                self._editTimer.Stop()

                        else:

                            self._editTimer = TreeEditTimer(self)

                        self._editTimer.Start(_DELAY, True)

                    self._lastOnSame = False


            else: # !RightDown() && !LeftUp() ==> LeftDown() || LeftDClick()

                if not item or not item.IsEnabled():
                    if self._editCtrl is not None and item != self._editCtrl.item():
                        self._editCtrl.StopEditing()
                    return

                if self._editCtrl is not None and item != self._editCtrl.item():
                    self._editCtrl.StopEditing()

                self._hasFocus = True
                self.SetFocusIgnoringChildren()

                if event.LeftDown():

                    self._lastOnSame = item == self._current

                if flags & TREE_HITTEST_ONITEMBUTTON:

                    # only toggle the item for a single click, double click on
                    # the button doesn't do anything (it toggles the item twice)
                    if event.LeftDown():

                        self.Toggle(item)

                    # don't select the item if the button was clicked
                    return

                if item.GetType() > 0 and (flags & TREE_HITTEST_ONITEMCHECKICON) and (flags & TREE_HITTEST_ONITEMLABEL == 0):

                    if event.LeftDown():
                        if flags & TREE_HITTEST_ONITEM and self.HasAGWFlag(TR_FULL_ROW_HIGHLIGHT):
                            self.DoSelectItem(item, not self.HasAGWFlag(TR_MULTIPLE))

                        if self.IsItem3State(item):
                            checked = self.GetItem3StateValue(item)
                            checked = (checked+1)%3
                        else:
                            checked = not self.IsItemChecked(item)

                        self.CheckItem(item, checked)

                    return

                # clear the previously selected items, if the
                # user clicked outside of the present selection.
                # otherwise, perform the deselection on mouse-up.
                # this allows multiple drag and drop to work.
                # but if Cmd is down, toggle selection of the clicked item
                if not self.IsSelected(item) or event.CmdDown():

                    if flags & TREE_HITTEST_ONITEM:
                        # how should the selection work for this event?
                        if item.IsHyperText():
                            self.SetItemVisited(item, True)

                        is_multiple, extended_select, unselect_others = EventFlagsToSelType(self.GetAGWWindowStyleFlag(),
                                                                                            event.ShiftDown(),
                                                                                            event.CmdDown())

                        self.DoSelectItem(item, unselect_others, extended_select)

                # Handle hyperlink items... which are a bit odd sometimes
                elif self.IsSelected(item) and item.IsHyperText():
                    self.HandleHyperLink(item)

                # For some reason, Windows isn't recognizing a left double-click,
                # so we need to simulate it here.  Allow 200 milliseconds for now.
                if event.LeftDClick():

                    # double clicking should not start editing the item label
                    if self._editTimer:
                        self._editTimer.Stop()

                    self._lastOnSame = False

                    # send activate event first
                    nevent = TreeEvent(wxEVT_TREE_ITEM_ACTIVATED, self.GetId())
                    nevent._item = item
                    nevent._pointDrag = self.CalcScrolledPosition(*pt)
                    nevent.SetEventObject(self)
                    if not self.GetEventHandler().ProcessEvent(nevent):

                        # if the user code didn't process the activate event,
                        # handle it ourselves by toggling the item when it is
                        # double clicked
##                        if item.HasPlus():
                        self.Toggle(item)


    def OnInternalIdle(self):
        """
        This method is normally only used internally, but sometimes an application
        may need it to implement functionality that should not be disabled by an
        application defining an `OnIdle` handler in a derived class.

        This method may be used to do delayed painting, for example, and most
        implementations call :meth:`wx.Window.UpdateWindowUI` in order to send update events
        to the window in idle time.
        """

        # Check if we need to select the root item
        # because nothing else has been selected.
        # Delaying it means that we can invoke event handlers
        # as required, when a first item is selected.
        if not self.HasAGWFlag(TR_MULTIPLE) and not self.GetSelection():

            if self._select_me:
                self.SelectItem(self._select_me)
            elif self.GetRootItem():
                self.SelectItem(self.GetRootItem())

        # after all changes have been done to the tree control,
        # we actually redraw the tree when everything is over

        if not self._dirty:
            return
        if self._freezeCount:
            return

        self._dirty = False

        self.CalculatePositions()
        self.Refresh()
        self.AdjustMyScrollbars()

#        event.Skip()


    def CalculateSize(self, item, dc, level=-1, align=0):
        """
        Calculates overall position and size of an item.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param `dc`: an instance of :class:`wx.DC`;
        :param integer `level`: the item level in the tree hierarchy;
        :param integer `align`: an integer specifying the alignment type:

         =============== =========================================
         `align` Value   Description
         =============== =========================================
                0        No horizontal alignment of windows (in items with windows).
                1        Windows (in items with windows) are aligned at the same horizontal position.
                2        Windows (in items with windows) are aligned at the rightmost edge of :class:`CustomTreeCtrl`.
         =============== =========================================

        """

        if self._freezeCount:
            # Skip calculate if frozen. Set dirty flag to do this when thawed.
            self._dirty = True
            return
        if item.IsHidden():
            # Hidden items have a height of 0.
            item.SetHeight(0)
            return

        attr = item.GetAttributes()

        if attr and attr.HasFont():
            dc.SetFont(attr.GetFont())
        else:
            if item.IsBold():
                dc.SetFont(self._boldFont)
            elif item.IsItalic():
                dc.SetFont(self._italicFont)
            else:
                dc.SetFont(self._normalFont)

        text_w, text_h, dummy = dc.GetFullMultiLineTextExtent(item.GetText())
        text_h+=2

        # restore normal font
        dc.SetFont(self._normalFont)

        image_w, image_h = 0, 0
        image = item.GetCurrentImage()

        if image != _NO_IMAGE:

            if self._imageListNormal:

                image_w, image_h = self._imageListNormal.GetSize(image)
                image_w += 4

        total_h = ((image_h > text_h) and [image_h] or [text_h])[0]

        checkimage = item.GetCurrentCheckedImage()
        if checkimage is not None:
            wcheck, hcheck = self._imageListCheck.GetSize(checkimage)
            wcheck += 4
        else:
            wcheck = 0

        if total_h < 30:
            total_h += 2            # at least 2 pixels
        else:
            total_h += total_h//10   # otherwise 10% extra spacing

        if total_h > self._lineHeight:
            self._lineHeight = total_h

        wnd = item.GetWindow()
        if not wnd:
            totalWidth = image_w+text_w+wcheck+2
            totalHeight = total_h
        else:
            totalWidth = item.GetWindowSize()[0]+image_w+text_w+wcheck+2
            totalHeight = max(total_h, item.GetWindowSize()[1])

        if level >= 0 and wnd:
            if align == 0:
                if level in self.absoluteWindows:
                    self.absoluteWindows[level] = max(self.absoluteWindows[level], image_w+text_w+wcheck+2)
                else:
                    self.absoluteWindows[level] = image_w+text_w+wcheck+2
            elif align == 1:
                self.absoluteWindows[level] = max(self.absoluteWindows[level], image_w+text_w+wcheck+2)

        if item.IsSeparator():
            totalWidth = self.GetClientSize()[0]
            totalHeight = total_h

        item.SetWidth(totalWidth)
        item.SetHeight(totalHeight)


    def CalculateLevel(self, item, dc, level, y, align=0):
        """
        Calculates the level of an item inside the tree hierarchy.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param `dc`: an instance of :class:`wx.DC`;
        :param integer `level`: the item level in the tree hierarchy;
        :param integer `y`: the current vertical position inside the :class:`ScrolledWindow`;
        :param integer `align`: an integer specifying the alignment type:

         =============== =========================================
         `align` Value   Description
         =============== =========================================
                0        No horizontal alignment of windows (in items with windows).
                1        Windows (in items with windows) are aligned at the same horizontal position.
                2        Windows (in items with windows) are aligned at the rightmost edge of :class:`CustomTreeCtrl`.
         =============== =========================================

        :return: The new `y` vertical position inside the :class:`ScrolledWindow`.
        """

        x = level*self._indent

        if not self.HasAGWFlag(TR_HIDE_ROOT):

            x += self._indent

        elif level == 0:

            # a hidden root is not evaluated, but its
            # children are always calculated
            children = item.GetChildren()
            count = len(children)
            level = level + 1
            for n in range(count):
                y = self.CalculateLevel(children[n], dc, level, y, align)  # recurse

            return y

        self.CalculateSize(item, dc, level, align)

        # set its position
        item.SetX(x+self._spacing)
        item.SetY(y)
        # hidden items don't get a height (height=0).
        if item.IsHidden():
            return y
        height = self.GetLineHeight(item)

        wnd = item.GetWindow()
        if wnd:
            # move its window, if necessary.
            xa, ya = self.CalcScrolledPosition((0, y))
            wndWidth, wndHeight = item.GetWindowSize()
            if height > wndHeight:
                ya += (height - wndHeight) // 2
            wndx, wndy = wnd.GetPosition()
            if wndy != ya:
                wnd.Move(wndx, ya, flags=wx.SIZE_ALLOW_MINUS_ONE)

        y += height

        if not item.IsExpanded():
            # we don't need to calculate collapsed branches
            return y

        children = item.GetChildren()
        count = len(children)
        level = level + 1
        for n in range(count):
            y = self.CalculateLevel(children[n], dc, level, y, align)  # recurse

        return y


    def CalculatePositions(self):
        """ Calculates all the positions of the visible items. """

        if not self._anchor:
            return
        if self._freezeCount:
            # Don't calculate positions if frozen as it is CPU intensive.
            self._dirty = True
            return

        self.absoluteWindows = {}

        dc = wx.ClientDC(self)
        self.PrepareDC(dc)

        dc.SetFont(self._normalFont)
        dc.SetPen(self._dottedPen)
        y = 2
        y = self.CalculateLevel(self._anchor, dc, 0, y) # start recursion

        if self.HasAGWFlag(TR_ALIGN_WINDOWS) or self.HasAGWFlag(TR_ALIGN_WINDOWS_RIGHT):
            align = (self.HasAGWFlag(TR_ALIGN_WINDOWS) and [1] or [2])[0]
            y = 2
            y = self.CalculateLevel(self._anchor, dc, 0, y, align) # start recursion


    def RefreshSubtree(self, item):
        """
        Refreshes a damaged subtree of an item.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        if self._dirty:
            return
        if self._freezeCount:
            return

        client = self.GetClientSize()

        rect = wx.Rect()
        x, rect.y = self.CalcScrolledPosition(0, item.GetY())
        rect.width = client.x
        rect.height = client.y

        self.Refresh(True, rect)
        self.AdjustMyScrollbars()


    def RefreshLine(self, item):
        """
        Refreshes a damaged item line.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        if self._dirty:
            return
        if self._freezeCount:
            return

        rect = wx.Rect()
        x, rect.y = self.CalcScrolledPosition(0, item.GetY())
        rect.width = self.GetClientSize().x
        rect.height = self.GetLineHeight(item)

        self.Refresh(True, rect)


    def RefreshSelected(self):
        """ Refreshes a damaged selected item line. """

        if self._freezeCount:
            return

        # TODO: this is awfully inefficient, we should keep the list of all
        #       selected items internally, should be much faster
        if self._anchor:
            self.RefreshSelectedUnder(self._anchor)


    def RefreshSelectedUnder(self, item):
        """
        Refreshes the selected items under the given item.

        :param `item`: an instance of :class:`GenericTreeItem`.
        """

        if self._freezeCount:
            return

        if item.IsSelected():
            self.RefreshLine(item)

        children = item.GetChildren()
        for child in children:
            self.RefreshSelectedUnder(child)


    def RefreshItemWithWindows(self, item=None):
        """
        Refreshes the items with which a window is associated.

        :param `item`: an instance of :class:`GenericTreeItem`. If `item` is ``None``, then the
         recursive refresh starts from the root node.

        :note: This method is called only if the style ``TR_ALIGN_WINDOWS_RIGHT`` is used.
        """

        if self._freezeCount:
            return

        if item is None:
            if self._anchor:
                self.RefreshItemWithWindows(self._anchor)
                return

        wnd = item.GetWindow()
        if wnd and wnd.IsShown():
            self.RefreshLine(item)

        children = item.GetChildren()
        for child in children:
            self.RefreshItemWithWindows(child)


    def Freeze(self):
        """
        Freeze :class:`CustomTreeCtrl`.

        Freezes the window or, in other words, prevents any updates from taking place
        on screen, the window is not redrawn at all. :meth:`~Thaw` must be called to re-enable
        window redrawing. Calls to these two functions may be nested.

        :note: This method is useful for visual appearance optimization (for example,
         it is a good idea to use it before doing many large text insertions in a row
         into a :class:`TextCtrl` under wxGTK) but is not implemented on all platforms nor
         for all controls so it is mostly just a hint to wxWidgets and not a mandatory
         directive.
        """
        ## Note: We manage freezing ourselves because a normal call to
        ##       Freeze() also freezes all child item windows and for
        ##       some reason this can cause them to glitch out.
        self._freezeCount = self._freezeCount + 1


    def Thaw(self):
        """
        Thaw :class:`CustomTreeCtrl`.

        Reenables window updating after a previous call to :meth:`~Freeze`. To really thaw the
        control, it must be called exactly the same number of times as :meth:`~Freeze`.

        :raise: `Exception` if :meth:`~Thaw` has been called without an un-matching :meth:`~Freeze`.
        """

        if self._freezeCount == 0:
            raise Exception("\nERROR: Thawing Unfrozen Tree Control?")

        self._freezeCount = self._freezeCount - 1

        if not self._freezeCount:
            self.Refresh()


    # ----------------------------------------------------------------------------
    # changing colours: we need to refresh the tree control
    # ----------------------------------------------------------------------------

    def SetBackgroundColour(self, colour):
        """
        Changes the background colour of :class:`CustomTreeCtrl`.

        :param `colour`: the colour to be used as the background colour, pass
         :class:`NullColour` to reset to the default colour.

        :return: ``False`` if the underlying :class:`ScrolledWindow` does not accept
         the new colour, ``True`` otherwise.

        :note: The background colour is usually painted by the default :class:`EraseEvent`
         event handler function under Windows and automatically under GTK.

        :note: Setting the background colour does not cause an immediate refresh, so
         you may wish to call :meth:`wx.Window.ClearBackground` or :meth:`wx.Window.Refresh` after
         calling this function.

        :note: Overridden from :class:`ScrolledWindow`.
        """

        if not wx.ScrolledWindow.SetBackgroundColour(self, colour):
            return False

        if self._freezeCount:
            return True

        self.Refresh()

        return True


    def SetForegroundColour(self, colour):
        """
        Changes the foreground colour of :class:`CustomTreeCtrl`.

        :param `colour`: the colour to be used as the foreground colour, pass
         :class:`NullColour` to reset to the default colour.

        :return: ``False`` if the underlying :class:`ScrolledWindow` does not accept
         the new colour, ``True`` otherwise.

        :note: Overridden from :class:`ScrolledWindow`.
        """

        if not wx.ScrolledWindow.SetForegroundColour(self, colour):
            return False

        if self._freezeCount:
            return True

        self.Refresh()

        return True


    def OnGetToolTip(self, event):
        """
        Process the tooltip event, to speed up event processing. Does not actually
        get a tooltip.

        :param `event`: a :class:`CommandTreeEvent` event to be processed.
        """

        event.Veto()


    def DoGetBestSize(self):
        """
        Gets the size which best suits the window: for a control, it would be the
        minimal size which doesn't truncate the control, for a panel - the same size
        as it would have after a call to `Fit()`.

        :return: An instance of :class:`wx.Size`.

        :note: Overridden from :class:`ScrolledWindow`.
        """

        # something is better than nothing...
        # 100x80 is what the MSW version will get from the default
        # wxControl::DoGetBestSize

        return wx.Size(100, 80)


    def GetMaxWidth(self, respect_expansion_state=True):
        """
        Returns the maximum width of the :class:`CustomTreeCtrl`.

        :param bool `respect_expansion_state`: if ``True``, only the expanded items (and their
         children) will be measured. Otherwise all the items are expanded and
         their width measured.

        :return: the maximum width of :class:`CustomTreeCtrl`, in pixels.
        """

        self.Freeze()

        root = self.GetRootItem()
        rect = self.GetBoundingRect(root, True)

        # It looks like the space between the "+" and the node
        # rect occupies 4 pixels approximately
        maxwidth = rect.x + rect.width + 4
        lastheight = rect.y + rect.height

        if not self.IsExpanded(root):
            if respect_expansion_state:
                return maxwidth

        if not respect_expansion_state:
            self.ExpandAll()

        maxwidth, lastheight = self.RecurseOnChildren(root, maxwidth, respect_expansion_state)

        self.Thaw()

        return maxwidth


    def RecurseOnChildren(self, item, maxwidth, respect_expansion_state):
        """
        Recurses over all the children of the spcified items, calculating their
        maximum width.

        :param `item`: an instance of :class:`GenericTreeItem`;
        :param integer `maxwidth`: the current maximum width for :class:`CustomTreeCtrl`, in pixels;
        :param bool `respect_expansion_state`: if ``True``, only the expanded items (and their
         children) will be measured. Otherwise all the items are expanded and
         their width measured.

        :return: A tuple containing the maximum width and item height, in pixels.
        """

        child, cookie = self.GetFirstChild(item)
        lastheight = 0

        while child:

            rect = self.GetBoundingRect(child, True)

            # It looks like the space between the "+" and the node
            # rect occupies 4 pixels approximately
            maxwidth = max(maxwidth, rect.x + rect.width + 4)
            lastheight = rect.y + rect.height

            if self.IsExpanded(child) or not respect_expansion_state:
                maxwidth, lastheight = self.RecurseOnChildren(child, maxwidth, respect_expansion_state)

            child, cookie = self.GetNextChild(item, cookie)

        return maxwidth, lastheight


    def GetClassDefaultAttributes(self):
        """
        Returns the default font and colours which are used by the control. This is
        useful if you want to use the same font or colour in your own control as in
        a standard control -- which is a much better idea than hard coding specific
        colours or fonts which might look completely out of place on the users system,
        especially if it uses themes.

        This static method is "overridden'' in many derived classes and so calling,
        for example, :meth:`Button.GetClassDefaultAttributes` () will typically return the
        values appropriate for a button which will be normally different from those
        returned by, say, :meth:`ListCtrl.GetClassDefaultAttributes` ().

        :return: An instance of :class:`VisualAttributes`.

        :note: The :class:`VisualAttributes` structure has at least the fields `font`,
         `colFg` and `colBg`. All of them may be invalid if it was not possible to
         determine the default control appearance or, especially for the background
         colour, if the field doesn't make sense as is the case for `colBg` for the
         controls with themed background.

        :note: Overridden from :class:`wx.Control`.
        """

        attr = wx.VisualAttributes()
        attr.colFg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
        attr.colBg = wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX)
        attr.font  = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        return attr

    GetClassDefaultAttributes = classmethod(GetClassDefaultAttributes)



if __name__ == '__main__':

    import wx

    class MyFrame(wx.Frame):

        def __init__(self, parent):

            wx.Frame.__init__(self, parent, -1, "CustomTreeCtrl Demo")

            # Create a CustomTreeCtrl instance
            custom_tree = CustomTreeCtrl(self, agwStyle=wx.TR_DEFAULT_STYLE)
            custom_tree.SetBackgroundColour(wx.WHITE)

            # Add a root node to it
            root = custom_tree.AddRoot("The Root Item")

            # Create an image list to add icons next to an item
            il = wx.ImageList(16, 16)
            fldridx     = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, (16, 16)))
            fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, (16, 16)))
            fileidx     = il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16)))

            custom_tree.SetImageList(il)

            custom_tree.SetItemImage(root, fldridx, wx.TreeItemIcon_Normal)
            custom_tree.SetItemImage(root, fldropenidx, wx.TreeItemIcon_Expanded)

            for x in range(15):
                child = custom_tree.AppendItem(root, "Item %d" % x)
                custom_tree.SetItemImage(child, fldridx, wx.TreeItemIcon_Normal)
                custom_tree.SetItemImage(child, fldropenidx, wx.TreeItemIcon_Expanded)

                for y in range(5):
                    last = custom_tree.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)))
                    custom_tree.SetItemImage(last, fldridx, wx.TreeItemIcon_Normal)
                    custom_tree.SetItemImage(last, fldropenidx, wx.TreeItemIcon_Expanded)

                    for z in range(5):
                        item = custom_tree.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z))
                        custom_tree.SetItemImage(item, fileidx, wx.TreeItemIcon_Normal)

            custom_tree.Expand(root)


    # our normal wxApp-derived class, as usual

    app = wx.App(0)
    locale = wx.Locale(wx.LANGUAGE_DEFAULT)
    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()
