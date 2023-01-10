
// Define path1 where exr files are located in subdirectories
var path1 = new String("C:\\Users\\Konain\\Documents\\HoudiniProjects\\Houdini_Normal_Pipeline\\renders\\test")
var topFolder = new Folder(path1);
var fileandfolderAr = scanSubFolders(topFolder, /\.(exr)$/i);
var fileList = fileandfolderAr[0];
var folderList = fileandfolderAr[1];

// DEFINE SUBSTRING OF FOLDER NAME HERE
var folderName = ""
if (folderName != "")
{
    // Find the folder containing substring in its name
    for (var i = 0; i < folderList.length; i++)
    {
        var currentFolderName = String(folderList[i]).split('/');
        
        for (var j = 0; j < currentFolderName.length; j++)
        {
            var substring = currentFolderName[j]
            list_of_substrings = substring.split('_')
            for (var k = 0; k < list_of_substrings.length; k++)
            {
                if (folderName == list_of_substrings[k])
                {
                    var path2 = path1 + "/" + substring
                    var topFolder1 = new Folder(path2);
                    var fileandfolderAr1 = scanSubFolders(topFolder1, /\.(exr)$/i);
                    var fileList1 = fileandfolderAr1[0];
    
                    for(var a = 0 ; a < fileList1.length; a++) 
                    {
                        open_exr(fileList1[a]);
                    }
                }
            }
        }
    }
}

else
{
    for(var a = 0 ; a < fileList.length; a++) 
    {
        open_exr(fileList[a]);
    }
}



function scanSubFolders(tFolder, mask) { // folder object, RegExp or string
    var sFolders = [];
    var allFiles = [];
    sFolders[0] = tFolder;
    for (var j = 0; j < sFolders.length; j++) { // loop through folders
        var procFiles = sFolders[j].getFiles();
        for (var i = 0; i < procFiles.length; i++) { // loop through this folder contents
            if (procFiles[i] instanceof File ) {
                if(mask == undefined) {
                    allFiles.push(procFiles); // if no search mask collect all files
                }
                if (procFiles[i].fullName.search(mask) != -1) {
                    allFiles.push(procFiles[i]); // otherwise only those that match mask
                }
            }
            else if (procFiles[i] instanceof Folder) {
                sFolders.push(procFiles[i]); // store the subfolder
                scanSubFolders(procFiles[i], mask); // search the subfolder
            }
        }
    }
    return [allFiles,sFolders];
}

function open_exr(path1)
{
    var idOpn = charIDToTypeID( "Opn " );
    var desc262 = new ActionDescriptor();
    var iddontRecord = stringIDToTypeID( "dontRecord" );
    desc262.putBoolean( iddontRecord, false );
    var idforceNotify = stringIDToTypeID( "forceNotify" );
    desc262.putBoolean( idforceNotify, true );
    var idnull = charIDToTypeID( "null" );
    desc262.putPath( idnull, new File( path1 ) );
    var idAs = charIDToTypeID( "As  " );
    var desc263 = new ActionDescriptor();
    var idAChn = charIDToTypeID( "AChn" );
    desc263.putInteger( idAChn, 0 );
    var idEXRf = charIDToTypeID( "EXRf" );
    desc262.putObject( idAs, idEXRf, desc263 );
    var idDocI = charIDToTypeID( "DocI" );
    desc262.putInteger( idDocI, 230 );
    executeAction( idOpn, desc262, DialogModes.NO );
}


