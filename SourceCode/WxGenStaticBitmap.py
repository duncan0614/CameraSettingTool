import wx

#----------------------------------------------------------------------

class GenStaticBitmap(wx.Control):
    """ :class:`GenStaticBitmap` is a generic implementation of :class:`wx.StaticBitmap`. """

    labelDelta = 1

    def __init__(self, parent, ID, bitmap,
                 pos = wx.DefaultPosition, size = wx.DefaultSize,
                 style = 0,
                 name = "genstatbmp"):
        """
        Default class constructor.

        :param `parent`: parent window, must not be ``None``;
        :param integer `ID`: window identifier. A value of -1 indicates a default value;
        :param wx.Bitmap `bitmap`: the static bitmap used in the control;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param integer `style`: the underlying :class:`wx.Control` style;
        :param string `name`: the widget name.

        :type parent: :class:`wx.Window`
        :type pos: tuple or :class:`wx.Point`
        :type size: tuple or :class:`wx.Size`
        """

        if not style & wx.BORDER_MASK:
            style = style | wx.BORDER_NONE

        wx.Control.__init__(self, parent, ID, pos, size, style,
                             wx.DefaultValidator, name)
        self._bitmap = bitmap
        self.InheritAttributes()
        self.SetInitialSize(size)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT,            self.OnPaint)


    def SetBitmap(self, bitmap):
        """
        Sets the bitmap label.

        :param wx.Bitmap `bitmap`: the new bitmap.

        .. seealso:: :meth:`GetBitmap`
        """

        self._bitmap = bitmap
        self.SetInitialSize( (bitmap.GetWidth(), bitmap.GetHeight()) )
        self.Refresh()


    def GetBitmap(self):
        """
        Returns the bitmap currently used in the control.

        :rtype: wx.Bitmap

        .. seealso:: :meth:`SetBitmap`
        """

        return self._bitmap


    def DoGetBestSize(self):
        """
        Overridden base class virtual.  Determines the best size of
        the control based on the label size and the current font.

        .. note:: Overridden from :class:`wx.Control`.
        """

        return wx.Size(self._bitmap.GetWidth(), self._bitmap.GetHeight())


    def AcceptsFocus(self):
        """
        Can this window be given focus by mouse click?

        .. note:: Overridden from :class:`wx.Control`.
        """

        return False


    def GetDefaultAttributes(self):
        """
        Overridden base class virtual.  By default we should use
        the same font/colour attributes as the native :class:`StaticBitmap`.

        .. note:: Overridden from :class:`wx.Control`.
        """

        return wx.StaticBitmap.GetClassDefaultAttributes()


    def ShouldInheritColours(self):
        """
        Overridden base class virtual.  If the parent has non-default
        colours then we want this control to inherit them.

        .. note:: Overridden from :class:`wx.Control`.
        """

        return True


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` for :class:`GenStaticBitmap`.

        :param `event`: a :class:`wx.PaintEvent` event to be processed.
        """

        dc = wx.PaintDC(self)
        if self._bitmap:
            dc.DrawBitmap(self._bitmap, 0, 0, True)


    def OnEraseBackground(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for :class:`GenStaticBitmap`.

        :param `event`: a :class:`wx.EraseEvent` event to be processed.

        .. note:: This is intentionally empty to reduce flicker.
        """

        pass
