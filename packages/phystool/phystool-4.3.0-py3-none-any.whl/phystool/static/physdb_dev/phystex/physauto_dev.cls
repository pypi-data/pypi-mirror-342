%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Originally created by Jérôme Dufour %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\ProvidesExplClass{physauto_dev}{2024/06/09}{1.0}
{ Minimal requirements to create PDBFile with phystool }
\LoadClass[12pt, a4paper]{article}

% CUSTOMIZE YOUR PACKAGES HERE
\RequirePackage[french]{babel}
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage{amssymb,amsmath}
\RequirePackage{graphicx}

% THE FOLLOWING THREE COMMANDS NEED TO EXIST, CHANGE THEM AT YOUR OWN RISK
\NewDocumentCommand{\PdbSetDBPath}{m}{
	\tl_gset:Nn \c_pdb_path_tl {#1}
}
\NewDocumentCommand{\PdbPrint}{m}{
	\group_begin:
		\file_input:n {\c_pdb_path_tl #1.tex}
	\group_end:
}
\NewDocumentCommand{\PdbTikz}{O{}m}{
	\includegraphics[#1]{#2}
}

\graphicspath{
	{\c_pdb_path_tl},  % to include Tikz figures managed by phystool
	{\c_pdb_path_tl figures}  % to include other figures
}


% THE FOLLOWING THREE ENVIRONENTS NEED TO EXIST, CHANGE THEM AT YOUR OWN RISK
\keys_define:nn {pdb_option}{
	title .tl_set:N = \l_pdb_title_tl,
}
\NewDocumentEnvironment{exercise}{o}{
	\IfValueTF{#1}{
		\keys_set:nn {pdb_option} {#1} 
		\subsection*{Exercice ~ \normalfont{\itshape{\l_pdb_title_tl}}}
	}{ \subsection*{Exercice} }
}{}
\NewDocumentEnvironment{theory}{o}{
	\IfValueTF{#1}{
		\keys_set:nn {pdb_option} {#1} 
		\subsection*{\l_pdb_title_tl}
	}{ \subsection*{Théorie} }
}{}
\NewDocumentEnvironment{tpstudent}{o}{
	\IfValueTF{#1}{
		\keys_set:nn {pdb_option} {#1} 
		\section*{TP ~ \normalfont\itshape {\l_pdb_title_tl}}
	}{ \subsection*{TP} }
}{}


%%%%%%%%%%%
%%% QCM %%%
%%%%%%%%%%%
\int_new:N \g_pdb_qcm_correct_prop_int
\seq_new:N \l_pdb_qcm_propositions_seq
\bool_set_false:N \l_pdb_qcm_shuffle_propositions_bool

\NewDocumentCommand{\qcmT}{m}{
	\seq_put_right:Nn \l_pdb_qcm_propositions_seq { \noindent $\checkmark$~ #1} 
	\int_gincr:N \g_pdb_qcm_correct_prop_int
}
\NewDocumentCommand{\qcmF}{m}{
	\seq_put_right:Nn \l_pdb_qcm_propositions_seq { \noindent $\square$~ #1 } 
}

\cs_new_protected:Nn \pdb_qcm_print:nnn {
	#1
	\par

	\bool_if:nT { \l_pdb_qcm_shuffle_propositions_bool && !#3 }
	{ \seq_gshuffle:N \l_pdb_qcm_propositions_seq }
	\int_zero:N \l_tmpa_int
	\seq_map_inline:Nn \l_pdb_qcm_propositions_seq {
		##1
		\int_incr:N \l_tmpa_int
		\int_compare:nNnTF{ \l_tmpa_int } = { #2 }
		{ \par \int_zero:N \l_tmpa_int }
		{ \hfill }
	}
}

\NewDocumentCommand{\QCM}{m+oO{0.4}msm}{
	\group_begin:
		\int_gzero:N \g_pdb_qcm_correct_prop_int
		\seq_clear:N \l_pdb_qcm_propositions_seq
		#6
		\pdb_qcm_print:nnn {#1} {#4} {#5} 
		#2
	\group_end:
}
