/*
 * GnomeSword Bible Study Tool
 * settings.h - SHORT DESCRIPTION
 *
 * Copyright (C) 2000,2001,2002 GnomeSword Developer Team
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Library General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 */

#ifndef _SETTINGS_H_
#define _SETTINGS_H_
/*
#ifdef HAVE_CONFIG_H
#include <config.h>
#endif
//#include <gnome.h>
#ifdef SUSE_10_2
#include <glib.h>
#else
#include <glib-2.0/glib.h>
#endif*/

#include <gconf/gconf-client.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct _settings SETTINGS;
struct _settings {
	char	
		*gs_version, 	/* GnomeSword version */
		*MainWindowModule,	/* module to open at program startup  */
		*CommWindowModule,	/* module to open at program startup  */
		*DictWindowModule,	/* module to open at program startup  */
	        *parallel1Module,	/* module to open at program startup  */
	        *parallel2Module,	/* module to open at program startup  */
	        *parallel3Module, /* module to open at program startup  */
	        *parallel4Module,	/* module to open at program startup  */
	        *parallel5Module, /* module to open at program startup  */
	        *personalcommentsmod,/* module to open at program startup  */
		sb_search_mod[80], 	/* module to use for sidebar search */
	        *devotionalmod, 	/* module to use for devotional */
	        *DefaultDict, 	/* module to use for devotional */
		*lex_greek, /* module to use for greek lexicon - strongs or thayers*/
		*lex_hebrew, /* module to use for hebrew lexicon - strongs or BDB*/	        
		*lex_greek_viewer, /* module to use for greek lexicon - strongs or thayers - in viewer */
		*lex_hebrew_viewer, /* module to use for hebrew lexicon - strongs or BDB - in viewer */
	        *currentverse,	/* verse to use at program startup */
		comm_key[80],	/*  */
	        *cvparallel,	/* current verse for detached parallel */
		*percomverse, /* current verse for personal comments */
	        *dictkey,		/* dictionary key to use at program startup - the one we shut down with */
	        *studypadfilename,   /* name of file in studypad when we closed */
		*studypaddir,	    /* directory for studypad files */
		groupName[50], /* shortcut bar group name (viewer, verse list) */
		searchText[256], /* search string used by sidebar search */
		findText[256],   /* string used by find dialog */
		*spell_language,
		
	/* fonts, font colors and font sizes */
	        *bible_text_color, /* color for text */
	        *bible_bg_color,  /* color for background */
	        *currentverse_color,  /* color for current verse */
	        *link_color,  /* color for strongs, morph tags */	
		*bible_verse_num_color, /* verse number color */
		*found_color, /* color to use for search word in results display */
		*font_color, /*  */
		*highlight_fg, /* special fg color when highlighting */
		*highlight_bg, /* special fg color when highlighting */
		*verse_num_font_size_str,
		*base_font_size_str;
		
	int
		verse_num_font_size,
		base_font_size,
      		sidebar_width,
		verselist_toppane_height, //height of the top pane in the search results window
		upperpane_hight,
		biblepane_width,
		biblepane_hight,
		commpane_hight,
		sidebar_notebook_hight,
		gs_width,
		tmp_width,
		gs_hight,	
		searchbargroup,      //-- number of search group in shortcut bar
		searchType,
		whichwindow,      	/* which of the main form html windows is active */
		intCurVerse,    /* detached parallel current verse */
		parallel_page,   /* parallel workbook page number */
		tab_page,   /* studypad workbook page number */
		percomm_page;   /* percomm editor workbook page number */
						
	int   
		usedefault, /* use default settings in gnomesword or those used for last session */
		strongs,	//-- toogle button and check menu state
		strongsint, //-- check menu state parallel mods
		headingsint, //-- check menu state parallel mods	
		crossrefint, //-- check menu state parallel mods	
		lemmasint, //-- check menu state parallel mods		
		morphsint, //-- check menu state parallel mods
		hebrewpointsint, //-- check menu state parallel mods
		cantillationmarksint, //-- check menu state parallel mods
	        footnotesint, //-- check menu state parallel mods
		greekaccentsint, //-- check menu state parallel mods
	        versestyle, /* use verse style if true or paragraph style if not */
	        pinnedtabs, /* all tabs are pinned together, moving in concert */
	        showversenum, /* display verse numbers in text (default on) */
	        readaloud, /* pass text through (existing) "festival -server" */
	        versehighlight, /* do special fg/bg for current verse */
	        doublespace, /* double-space text (default off) */
	        parallelpage, /* display parallel page */
	        autosavepersonalcomments, /* auto save personal notes */
	        formatpercom, /* use html to format personal notes */
	        showshortcutbar, /* display shortcut bar if true */
	        showsidebar, /* display sidebar bar if true */
		showfavoritesgroup, /* display shortcut bar group if true */
	        showtextgroup, /* display shortcut bar group if true */
	        showcomgroup, /* display shortcut bar group if true */
	        showdictgroup, /* display shortcut bar group if true */
	        showbookgroup, /* display shortcut bar group if true */
	        showbookmarksgroup, /* display shortcut bar group if true */
	        showhistorygroup, /* display shortcut bar group if true */
		showsplash, /* show splash on program start if true */
		showdevotional, /* show devotional on program start if true */
		text_tool, /* show toolbar in text window if true  */
                showtexts, /* show bible texts if true  */
                showpreview, /* show preview pane if true  */
                showcomms, /* show commentaries if true  */
                showdicts, /* show dictionaries/lexicons if true */
		displaySearchResults, /* are we displaying search results in chap display */
		showinmain, /* when verse list item clicked show in main form if true */
		havethayer, /* for greek morph tags */
		havebdb, /* for hebrew morph tags */
//		inViewer, /* display dict/lex in viewer when word or link clicked */
//		inDictpane, /* display dict/lex in Dict/Lex pane when word or link clicked */
		useDefaultDict,
//		strip_words_in_red,
		browsing, /* true for tabbed browsing */
		
		/** if items are docked **/
		docked, /* true when sidebar is docked */
		dockedInt, /* true when parallel page is docked */
		
		/**  find dialogs info  **/
		finddialog, /* if finddialog open (showing) */
		
		/** editors **/
		editnote, /* true when percom html widget is in edit mode */
		editgbs, /* true when gbs html widget is in edit mode */
		modifiedGBS, /* book entry modified */
		modifiedPC, /* personal note modified */
		modifiedSP, /* studypad file modified */
//		use_studypad, /* use studypad */
//		use_studypad_dialog, /* display studypad in a dialog */
		studypad_dialog_exist, /* studypad dialog has been created */
//		use_percomm_dialog, /* display personal comments editor in a dialog */
		percomm_dialog_exist, /* percomm dialog has been created */
		
		/** do we have these modules **/
		havebible, 
		havecomm, 
		havedict, 
		havebook, 
		havepercomm,
		haveprayerlist,
		/* do we need to add item to history */
		addhistoryitem;
	
	
		
	/* gbs */	
	char *book_mod;	/* module to open at program startup  */
	char *book_key;    /*  */
	unsigned long book_offset;
	
	
	int comm_showing;
	
	/* store program title */
	char program_title[256];
	
	/* store $home directory */
	char *homedir;

	/* store .gnomesword-2.0 directory */
	char *gSwordDir;

	/* bookmarks directory */
	char *swbmDir;

	/* store dir name for shortcutbar files */
	char *shortcutbarDir;

	/* store filename for configure file - options */
	char *fnconfigure;

	/* module name for current dialog */
	char *module_dialog;

	/* apply changes to what? the text navigation bar */
	int apply_change;
	
	/* load xml bookmarks */
	int load_xml_bookmarks;
	
	/* is Bibletime on the system */
	int have_bibletime;
	
	/* cell height of dictionary treeview */
	int cell_height;
	
	/* window location at close */
	int app_x;
	int app_y;
	
	/* set up druid canceled */
	int setup_canceled;
	
	/* there is no settings.xml file */
	int first_run;
	
	/* widget shadow type */
	int shadow_type;
	
	/* chapter scroll */
	int chapter_scroll;
	
	/* auto image resize in com/book/dict */
	int imageresize;
	
	/* signal id dictionary combo changed */
	long signal_id;
	
};

extern SETTINGS settings;

int settings_init(int new_configs, int new_bookmarks);
void load_settings_structure(void);
void gconf_setup(void);

#define	GS_GCONF_MAX	6

#ifdef __cplusplus
}
#endif

#endif
