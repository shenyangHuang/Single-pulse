## Automatically adapted for numpy Apr 14, 2006 by convertcode.py

## Automatically adapted for numpy Apr 14, 2006 by convertcode.py

# Routine for easy to use 1-D and 2-D plotting using 'PGPLOT'
#       and the Python 'PPGPLOT' package
#
# Written by Scott M. Ransom (ransom@cfa.harvard.edu)
#          last revision: 01 Jul 2000
#
# 'PGPLOT' was writtten by Tim Pearson <tjp@astro.caltech.edu>,
# and can be found at http://astro.caltech.edu/~tjp/pgplot/
#
# 'PPGPLOT' was written by Nick Patavalis <npat@ariadne.di.uoa.gr>,
# and can be found at http://ariadne.di.uoa.gr/ppgplot/
# _or_ an updated version is available in the same directory
# where this file was found:  ftp://cfa-ftp.harvard.edu/pub/ransom 
#

import numpy as Num
import types, math, ppgplot
import fileinput
import glob
# True if we have an /XWIN or /XSERVE device open yet
ppgplot_dev_open_ = 0

# True if we have already scaled and/or prepped the current page
ppgplot_dev_prep_ = 0

# Default plotting device
ppgplot_device_ = '/XWIN'

# Default font to use
ppgplot_font_ = 1

# Default font size to use
ppgplot_font_size_ = 1.0

# Default line style to use
ppgplot_linestyle_ = 1

# Default line width to use
ppgplot_linewidth_ = 2

# Default symbol to plot
ppgplot_symbol_ = None

# Default label color for contour lines
ppgplot_labels_ = None

# Default label interval for labeling contour lines
ppgplot_labelint_ = 20

# Default minimum label interval for labeling contour lines
ppgplot_labelmin_ = 20

# Default line colors to use
ppgplot_color_ = 'white'

# Default color palette for IMAG routines
ppgplot_palette_ = 'rainbow'

# The set of colors for PGPLOT
ppgplot_colors_ = { \
    'black':0, 'Black':0, 'BLACK':0, \
    'white':1, 'White':1, 'WHITE':1, \
    'red':2, 'Red':2, 'RED':2, \
    'green':3, 'Green':3, 'GREEN':3, \
    'blue':4, 'Blue':4, 'BLUE':4, \
    'cyan':5, 'Cyan':5, 'CYAN':5, \
    'magenta':6, 'Magenta':6, 'MAGENTA':6, \
    'yellow':7, 'Yellow':7, 'YELLOW':7, \
    'orange':8, 'Orange':8, 'ORANGE':8, \
    'green2':9, 'Green2':9, 'GREEN2':9, \
    'green3':10, 'Green3':10, 'GREEN3':10, \
    'blue2':11, 'Blue2':14, 'BLUE2':11, \
    'purple':12, 'Purple':12, 'PURPLE':12, \
    'pink':13, 'Pink':13, 'PINK':13, \
    'darkgray':14, 'DarkGray':14, 'DARKGRAY':14, \
    'dark gray':14, 'Dark Gray':14, 'DARK GRAY':14, \
    'lightgray':15, 'LightGray':15, 'LIGHTGRAY':15, \
    'light gray':15, 'Light Gray':15, 'LIGHT GRAY':15 \
    }

# Show a 2D color intensity plot with optional arguments and keywords
def plot_waterfall(z, x=None, y=None, title=None, rangex=None, rangey=None, \
           rangez=None, labx='', laby='', rangex2=None, rangey2=None, \
           labx2='', laby2='', image=ppgplot_palette_, contours=None, \
           logx=0, logy=0, logx2=0, logy2=0, \
           line=ppgplot_linestyle_, width=ppgplot_linewidth_, \
           color=ppgplot_color_, labels=ppgplot_labels_, \
           labelint=ppgplot_labelint_, labelmin=ppgplot_labelmin_, \
           font=ppgplot_font_, id=0, noscale=0, aspect=1, \
           fontsize=ppgplot_font_size_, ticks='out', panels=[1,1], \
           device=ppgplot_device_):
    """
    plot2d waterfall plot(z, ...)
        An interface to make various 2D plots using PGPLOT.
            'z' is the 2D Numpy array to be plotted.
        The optional entries are:
            x:         x values                    (default = 0, 1, ...) 
            y:         y values                    (default = 0, 1, ...) 
            title:     graph title                 (default = None)      
            rangex:    range for the x-axis        (default = automatic) 
            rangey:    range for the y-axis        (default = automatic) 
            rangez:    range for the z-axis        (default = automatic) 
            labx:      label for the x-axis        (default = None)      
            laby:      label for the y-axis        (default = None)      
            rangex2:   range for 2nd x-axis        (default = None)      
            rangey2:   range for 2nd y-axis        (default = None)      
            labx2:     label for the 2nd x-axis    (default = None)      
            laby2:     label for the 2nd y-axis    (default = None)      
            logx:      make the 1st x-axis log     (default = 0 (no))
            logy:      make the 1st y-axis log     (default = 0 (no))
            logx2:     make the 2nd x-axis log     (default = 0 (no))
            logy2:     make the 2nd y-axis log     (default = 0 (no))
            image:     color palette for image     (default = 'rainbow') 
            contours:  list of contour values      (default = None)      
            line:      contour line style          (default = 1 (solid)) 
            width:     contour line width          (default = 1 (thin))  
            color:     contour line color          (default = 'white')   
            labels:    color of contour labels     (default = None)      
            labelint:  contour label spacing       (default = 20)        
            labelmin:  min contour label spacing   (default = 20)        
            font:      PGPLOT font to use          (default = 1 (normal))
            fontsize:  PGPLOT font size to use     (default = 1.0 (normal))
            id:        show ID line on plot        (default = 0 (no))    
            noscale:   turn off auto scaling       (default = 0 (no))    
            aspect:    Aspect ratio                (default = 1 (square))
            ticks:     Ticks point in or out       (default = 'out')   
            panels:    Number of subpanels [r,c]   (default = [1,1])
            device:    PGPLOT device to use        (default = '/XWIN')   
        Note:  Many default values are defined in global variables
            with names like ppgplot_font_ or ppgplot_device_.
   """
    # Make sure the input data is a 2D array
    z = Num.asarray(z);
    if not len(z.shape)==2:
        print 'Input data array must be 2 dimensional.'
        return
    # Announce the global variables we will be using
    global ppgplot_dev_open_, ppgplot_dev_prep_, pgpalette
    # Define the X and Y axis limits if needed
    if x is None: x=Num.arange(z.shape[1], dtype='f')
    else: x = Num.asarray(x)
    if y is None: y=Num.arange(z.shape[0], dtype='f')
    else: y = Num.asarray(y)
    # Determine the scaling to use for the axes
    if rangex is None:
        dx =  x[-1]-x[-2]
        rangex=[x[0], x[-1]+dx]
    if rangey is None:
        dy =  y[-1]-y[-2]
        rangey=[y[0], y[-1]+dy]
    if rangez is None: rangez=[Num.minimum.reduce(Num.ravel(z)), \
                             Num.maximum.reduce(Num.ravel(z))]
    if image is not None:
        # Set the color indices and the color table
        lo_col_ind, hi_col_ind = ppgplot.pgqcol()
        lo_col_ind = lo_col_ind + 2
        ppgplot.pgscir(lo_col_ind, hi_col_ind)
        pgpalette.setpalette(image)
        ppgplot.pgctab(pgpalette.l,pgpalette.r,pgpalette.g,pgpalette.b)
        # Construct the image
        ppgplot.pggray_s(z, 0.0, 0.0, rangex[0], rangey[0], \
                         rangex[1], rangey[1])  

def read_sp_files(files):
    """Read all *.singlepulse files in the current directory in a DM range.
        Return 5 arrays (properties of all single pulses):
                DM, sigma, time, sample, downfact."""
    finput = fileinput.input(files)
    data = Num.loadtxt(finput,
                       dtype=Num.dtype([('dm', 'float32'),
                                        ('sigma','float32'),
                                        ('time','float32'),
                                        ('sample','uint32'),
                                        ('downfact','uint8')]))
    return Num.atleast_2d(data)

def read_tarfile(filenames, names, tar):
    members = []
    for name in names:
        if name in filenames:
            member = tar.getmember(name)
            members.append(member)
        else:
            pass
    fileinfo = []
    filearr = []
    for mem in members:
        file = tar.extractfile(mem)
        for line in file.readlines():
            fileinfo.append(line)
        filearr+=(fileinfo[1:])
        fileinfo = []
    temp_list = []
    for i in range(len(filearr)):
        temp_line = filearr[i].split()
        temp_list.append(temp_line)
    main_array = Num.asarray(temp_list)
    main_array = Num.split(main_array, 5, axis=1)
    main_array[0] = main_array[0].astype(Num.float16)
    main_array[1] = main_array[1].astype(Num.float16)
    main_array[2] = main_array[2].astype(Num.float16)
    main_array[3] = main_array[3].astype(Num.int)
    main_array[4] = main_array[4].astype(Num.int)
    return main_array
def gen_arrays(dm, threshold, sp_files, tar = None):    
    """
    Extract dms, times and signal to noise from each singlepulse file as 1D arrays.
    """
    max_dm = Num.ceil(Num.max(dm)).astype('int')
    min_dm = Num.min(dm).astype('int')
    diff_dm = max_dm-min_dm
    ddm = min_dm-diff_dm
    if (ddm <= 0):
        ddm = 0
    dmss = Num.zeros((1,)).astype('float32')
    timess = Num.zeros((1,)).astype('float32')
    sigmass = Num.zeros((1,)).astype('float32')
    ind = []
    dm_time_files = []
    for i in range(ddm,(max_dm+diff_dm)):
        """after DM of 1826 the dm step size is >=1, therefore we need to pick the correct DMs."""
        if (i >= 1826) and (i < 3266):
            if int(i)%2 == 1:
                i = i+1
            try:
                singlepulsefiles = [sp_files[sp_file] for sp_file in range(len(sp_files)) if ('DM'+str(i)+'.') in sp_files[sp_file]]
                dm_time_files += singlepulsefiles
                if tar is not None:
                    data = read_tarfile(sp_files, singlepulsefiles, tar)
                else:
                    data = read_sp_files(singlepulsefiles)[0]
            except:
                pass
        elif (i >= 3266) and (i < 5546):
            if int(i)%3 == 0:
                i = i+2
            if int(i)%3 == 1:
                i = i+1
            try:
                singlepulsefiles = [sp_files[sp_file] for sp_file in range(len(sp_files)) if ('DM'+str(i)+'.') in sp_files[sp_file]]
                dm_time_files += singlepulsefiles
                if tar is not None:
                    data = read_tarfile(sp_files, singlepulsefiles, tar)
                else:
                    data = read_sp_files(singlepulsefiles)[0]
            except:
                pass
        elif i>=5546:
            if int(i)%5 == 2:
                i = i+4
            if int(i)%5 == 3:
                i = i+3
            if int(i)%5 == 4:
                i = i+2
            if int(i)%5 == 0:
                i = i+1
            try:
                singlepulsefiles = [sp_files[sp_file] for sp_file in range(len(sp_files)) if ('DM'+str(i)+'.') in sp_files[sp_file]]
                dm_time_files += singlepulsefiles
                if tar is not None:
                    data = read_tarfile(sp_files, singlepulsefiles, tar)
                else:
                    data = read_sp_files(singlepulsefiles)[0]
            except:
                pass
        else:    
            try:
                singlepulsefiles = [sp_files[sp_file] for sp_file in range(len(sp_files)) if ('DM'+str(i)+'.') in sp_files[sp_file]]
                dm_time_files += singlepulsefiles
                if tar is not None:
                    data = read_tarfile(sp_files, singlepulsefiles, tar)
                else:
                    data = read_sp_files(singlepulsefiles)[0]
            except:
                pass
        if tar is not None:
            dms = Num.reshape(data[0],(len(data[0]),))
            times = Num.reshape(data[2],(len(data[1]),))
            sigmas = Num.reshape(data[1],(len(data[2]),))
        else:
            dms = data['dm']
            times = data['time']
            sigmas = data['sigma']
        dms = Num.concatenate((dmss, dms), axis = 0)
        dmss = dms
        times = Num.concatenate((timess, times), axis = 0)
        timess = times
        sigmas = Num.concatenate((sigmass, sigmas), axis = 0)
        sigmass = sigmas
    dms = Num.delete(dms, (0), axis = 0)
    times = Num.delete(times, (0), axis = 0)
    sigmas = Num.delete(sigmas, (0), axis = 0)
    return dms, times, sigmas, dm_time_files

def dm_time_plot(dms, times, sigmas, dm_arr, sigma_arr, time_arr, Total_observed_time):
    """
    Plot DM vs Time.
    """
    min_dm = Num.min(dms)
    max_dm = Num.max(dms)
    ppgplot.pgsvp(0.48, 0.97, 0.1, 0.54)
    ppgplot.pgswin(0, Total_observed_time, min_dm, max_dm)
    ppgplot.pgsch(0.8)
    ppgplot.pgslw(3)
    ppgplot.pgbox("BCNST", 0, 0, "BCNST", 0, 0)
    ppgplot.pgslw(3)
    ppgplot.pgmtxt('B', 2.5, 0.5, 0.5, "Time (s)")
    ppgplot.pgmtxt('L', 1.8, 0.5, 0.5, "DM (pc cm\u-3\d)")
    snr_range = 12.0
    cand_symbols = []
    cand_symbols_group = []
    for i in range(len(sigmas)):
        if sigmas[i] > 20.00:
            sigmas[i] = 20.0
        cand_symbol = int((sigmas[i] - 5.0)/snr_range * 6.0 + 20.5)
        cand_symbols.append(min(cand_symbol, 26))
    cand_symbols = Num.array(cand_symbols)
    for i in range(len(dm_arr)):
        cand_symbol = int((sigma_arr[i] - 5.0)/snr_range * 6.0 + 20.5)
        cand_symbols_group.append(min(cand_symbol, 26))
    cand_symbols_group = Num.array(cand_symbols_group)
    dms = Num.array(dms)
    times = Num.array(times)
    dm_arr = Num.array(dm_arr)
    time_arr = Num.array(time_arr)
    for ii in [26, 25, 24, 23, 22, 21, 20]:
        inds = Num.nonzero(cand_symbols == ii)[0]
        ppgplot.pgshls(1, 0.0, 0.5, 0.0)
        ppgplot.pgpt(times[inds], dms[inds], ii)
    for ii in [26, 25, 24, 23, 22, 21, 20]:
        inds_1 = Num.nonzero(cand_symbols_group == ii)[0]
        ppgplot.pgshls(1, 0.0, 0.0, 0.0)
        ppgplot.pgpt(time_arr[inds_1], dm_arr[inds_1], ii)

#########################################################################

class Palette:
    # Set the color palette
    def setpalette(self, palette):
        """
        setpalette(self, palette):
            Set the color palette for imag-style routines
        """
        if (palette == 'rainbow'):
            self.l = Num.array([0.0, 0.015, 0.225, 0.4, 0.59,
                                0.6, 0.775, 0.955, 0.965, 1.0])
            self.r = Num.array([1.0, 1.0, 1.0, 0.0, 0.0,
                                0.0, 0.0, 0.947, 1.0, 1.0])
            self.g = Num.array([0.0, 0.0, 1.0, 1.0, 1.0,
                                0.946, 0.0, 0.8, 0.844, 1.0])
            self.b = Num.array([0.0, 0.0, 0.0, 0.0, 0.95,
                                1.0, 1.0, 1.0, 1.0, 1.0])
        elif (palette == 'antirainbow'):
            self.l = Num.array([0.0, 0.035, 0.045, 0.225, 0.4,
                                0.41, 0.6, 0.775, 0.985, 1.0])
            self.r = Num.array([1.0, 1.0, 0.947, 0.0, 0.0,
                                0.0, 0.0, 1.0, 1.0, 1.0])
            self.g = Num.array([1.0, 0.844, 0.8, 0.0, 0.946,
                                1.0, 1.0, 1.0, 0.0, 0.0])
            self.b = Num.array([1.0, 1.0, 1.0, 1.0, 1.0,
                                0.95, 0.0, 0.0, 0.0, 0.0])
        elif (palette == 'astro'):
            self.l = Num.array([0.0, 0.167, 0.333, 0.5,
                                0.667, 0.833, 1.0])
            self.r = Num.array([0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0])
            self.g = Num.array([0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0])
            self.b = Num.array([0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0])
        elif (palette == 'hue'):
            self.l = Num.array([0.0, 0.167, 0.333, 0.5,
                                0.667, 0.833, 1.0])
            self.r = Num.array([1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0])
            self.g = Num.array([0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
            self.b = Num.array([0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0])
        elif (palette == 'heat'):
            self.l = Num.array([0.0, 0.48, 0.7, 0.75, 1.0])
            self.r = Num.array([0.0, 1.0, 1.0, 1.0, 1.0])
            self.g = Num.array([0.0, 0.0, 0.423, 0.519, 1.0])
            self.b = Num.array([0.0, 0.0, 0.0, 0.0, 1.0])
        elif (palette == 'gamma'):
            self.l = Num.array([0.0, 0.33, 0.66, 1.0])
            self.r = Num.array([0.3, 1.0, 0.0, 0.0])
            self.g = Num.array([0.0, 0.3, 1.0, 0.0])
            self.b = Num.array([0.0, 0.0, 0.3, 1.0])
        elif (palette == 'antigray' or palette == 'antigrey'):
            self.l = Num.array([0.0, 1.0])
            self.r = Num.array([1.0, 0.0])
            self.g = Num.array([1.0, 0.0])
            self.b = Num.array([1.0, 0.0])
        elif (palette == 'apjgray' or palette == 'apjgrey'):
            self.l = Num.array([0.0, 1.0])
            self.r = Num.array([1.0, 0.25])
            self.g = Num.array([1.0, 0.25])
            self.b = Num.array([1.0, 0.25])
        else:
            self.l = Num.array([0.0, 1.0])
            self.r = Num.array([0.0, 1.0])
            self.g = Num.array([0.0, 1.0])
            self.b = Num.array([0.0, 1.0])

pgpalette = Palette()


