
#   Some utility functions
import os, os.path

PYTHON_MARKER = "# CAN_EDIT_AFTER_THIS_LINE"
ZCML_MARKER = "<!-- CAN_EDIT_AFTER_THIS_LINE -->"

def parseCmdLine(cmdLine):
    """Roll my own parser, so that I don't have to be final about the
    valid options"""
    files=[]
    modifiers=[]
    for i in range(len(cmdLine)):
        arg = cmdLine[i]
        if arg[:2] != '--':
            files = cmdLine[i:]
            return (modifiers, files)
            
        arg = arg[2:]
        parts = arg.split('=',1)
        modifiers.append((parts[0], parts[1]))
    return (modifiers, files)


def BuildPath(DSLModel, table):
    """Create target folders if necessary"""
    folders = [
        DSLModel['GENERAL']['target_folder'],
        "%s%s%s" % (DSLModel['GENERAL']['target_folder'], os.sep, table['name'])
        ]
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)
        init_path = folder + os.sep + '__init__.py'
        if not os.path.exists(init_path):
            fh = open(init_path, 'w')
            fh.write('# Module Initialiation File')
            fh.close()
    TemplatesPath = "%s%s%s%stemplates" % (DSLModel['GENERAL']['target_folder'], os.sep, table['name'],
        os.sep)
    if not os.path.exists(TemplatesPath):
        os.mkdir(TemplatesPath)


def MergeUserChanges(oldcontent, newcontent, marker):
    """Copy user changes from old file to new file.
    User changes are signified by a comment, PYTHON_MARKER or ZCML_MARKER
    """
    oldlines = oldcontent.split('\n')
    oldedits = None
    for i in range(len(oldlines)):
        line = oldlines[i]
        if line.find(marker) != -1:
            oldedits = oldlines[i+1:]
    if not oldedits:
        # Nothing in the old
        return newcontent
    newlines = newcontent.split('\n')
    for i in range(len(newlines)):
        line = newlines[i]
        if line.find(marker) != -1:
            # Found it - append and return
            newlines = newlines[:i+1] + oldedits
            return '\n'.join(newlines)
    return newcontent

def FileExists(DSLModel, table, filename):
    """Test whether a file exists"""
    fullpath="%s%s%s%s%s" % (DSLModel['GENERAL']['target_folder'], os.sep,
        table['name'], os.sep, filename)
    return os.access(fullpath, os.F_OK)

def ReplaceFile(DSLModel, table, filename, content, format="python"):
    fullpath="%s%s%s%s%s" % (DSLModel['GENERAL']['target_folder'], os.sep,
        table['name'], os.sep, filename)

    # replace tabs - more convenient for editing after
    content = content.replace('\t', '    ')
    if os.access(fullpath, os.F_OK):
        # File already exists.
        # First merge any changes from the original file into content
        fh = open(fullpath)
        oldcontent = fh.read()
        fh.close()

        if format == 'python':
            content = MergeUserChanges(oldcontent, content, marker=PYTHON_MARKER)
        elif format == 'zcml':
            content = MergeUserChanges(oldcontent, content, marker=ZCML_MARKER)

        if content == oldcontent:
            return # No change

        # Back-up old file
        backup=fullpath+'~'
        if os.access(backup, os.F_OK):
            os.unlink(backup)
        os.rename(fullpath, backup)

    fh = open(fullpath, 'w')
    fh.write(content)
    fh.close()

def AddNewPackage(path, package_name, namespace):
    """Add the new package to the list of packages.
    Will normally be there already."""

    new_line = '<include package=".%s" />' % package_name
    fullpath=path + '/configure.zcml'

    try:
        fh=open(fullpath)
        lines=fh.readlines()
        for i in range(len(lines)):
            if len(lines[i]) == 0: continue
            if lines[i][-1] in ['\n', '\r']: lines[i] = lines[i][:-1]
            if len(lines[i]) == 0: continue
            if lines[i][-1] in ['\n', '\r']: lines[i] = lines[i][:-1]
        fh.close()
    except:
        lines=[
        '<configure',
            '\txmlns="http://namespaces.zope.org/zope"',
            '\ti18n_domain="%s">\n' % namespace, 
            '\t<!-- END OF PACKAGES -->',
        '\n</configure>']


    # See if our file is present
    for l in lines:
        if l.find(new_line) != -1:
            return # all done

    # Find the marker and insert at that point
    for i in range(len(lines)):
        l = lines[i]
        if l.find('<!-- END OF PACKAGES -->') != -1:
            lines = lines[:i] + ['\t'+new_line] + lines[i:]
            break

    # rewrite the file       
    if os.access(fullpath, os.F_OK):
        backup=fullpath+'~'
        if os.access(backup, os.F_OK):
            os.unlink(backup)
        os.rename(fullpath, backup)

    fh = open(fullpath, 'w')
    fh.write('\n'.join([l.replace('\t', '    ') for l in lines]))
    fh.close()


def ImportTemplate(template_names):
    """Work through the names and try each until an import works. Then
    return the imported file"""
    for file in template_names:
        try:
            return __import__(file)
        except ImportError:
            pass
    raise ImportError, 'No files matching %s' % template_names
