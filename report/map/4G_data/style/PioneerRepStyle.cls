\ProvidesClass{PioneerRepStyle}[2021/07/27]
\makeatletter
\def\@classoptionslist{oneside,landscape,openany}
\makeatother
\LoadClass[oneside]{book}

%----------------------------------------------------------------------------------------
%	Add Packages

\usepackage{graphicx}
%\usepackage{csvsimple} %Add CSV file
\usepackage{longtable}
\usepackage{booktabs} % Required for nicer horizontal rules in tables
%\usepackage{enumitem} % Customize lists

\usepackage{geometry} % Required for adjusting page dimensions and margins
\geometry{
	paper=a4paper, % Paper size, change to letterpaper for US letter size
	top=1.2cm, % Top margin
	bottom=1cm, % Bottom margin
	left=0.6cm, % Left margin
	right=0.6cm, % Right margin
	headheight=30pt, % Header height
	footskip=1.4cm, % Space from the bottom margin to the baseline of the footer
	headsep=6pt, % Space from the top margin to the baseline of the header
	%showframe, % Uncomment to show how the type block is set on the page
}

%\usepackage{scrextend}
%\usepackage{xstring} %For if and else condition
%\usepackage{xparse} %For define newcommand

\usepackage[dvipsnames,table]{xcolor} % Required for specifying colors by name
% Define the orange color used for highlighting throughout the book
\definecolor{ocre}{RGB}{243,102,25} 

\usepackage{subcaption}
\usepackage{tikz} % Required for drawing custom shapes
\usepackage{float}
\usepackage[yyyymmdd,hhmmss]{datetime}
\usepackage[font={Large}]{caption}
\usepackage{multicol}
\setlength{\columnseprule}{.4pt}
%\addtokomafont{labelinglabel}{\sffamily}

\usepackage{avant} % Use the Avantgarde font for headings
%\usepackage{times} % Use the Times font for headings
\usepackage{mathptmx} % Use the Adobe Times Roman as the default text font together with math symbols from the Sym­bol, Chancery and Com­puter Modern fonts
\usepackage{microtype} % Slightly tweak font spacing for aesthetics
%\usepackage[utf8]{inputenc} % Required for including letters with accents
%\usepackage[T1]{fontenc} % Use 8-bit encoding that has 256 glyphs

%\usepackage{calc} % For simpler calculation - used for spacing the index letter headings correctly
\usepackage{titletoc} % Required for manipulating the table of contents
\contentsmargin{0cm} % Removes the default margin

% Chapter text styling
\titlecontents{chapter}
	[1.25cm] % Left indentation
	{\addvspace{12pt}\large\sffamily\bfseries} % Spacing and font options for chapters
	{\color{ocre!60}\contentslabel[\Large\thecontentslabel]{1.25cm}\color{ocre}} % Formatting of numbered sections of this type
	{\color{ocre}} % Formatting of numberless sections of this type
	{\color{ocre!60}\normalsize\titlerule*[.5pc]{.}\thecontentspage} % Formatting of the filler to the right of the heading and the page number

% Section text styling
\titlecontents{section}
	[1.25cm] % Left indentation
	{\addvspace{1pt}\sffamily\bfseries\small} % Spacing and font options for sections
	{\contentslabel[\thecontentslabel]{1.25cm}} % Formatting of numbered sections of this type
	{} % Formatting of numberless sections of this type
	{\hfill\color{black}\thecontentspage} % Formatting of the filler to the right of the heading and the page number

% Subsection text styling
\titlecontents{subsection}
	[1.25cm] % Left indentation
	{\addvspace{1pt}\sffamily\small} % Spacing and font options for subsections
	{\contentslabel[\thecontentslabel]{1.25cm}} % Formatting of numbered sections of this type
	{} % Formatting of numberless sections of this type
	{\ \titlerule*[.5pc]{.}\thecontentspage} % Formatting of the filler to the right of the heading and the page number

% Figure text styling
\titlecontents{figure}
	[1.25cm] % Left indentation
	{\addvspace{1pt}\sffamily} % Spacing and font options for figures
	{\thecontentslabel\hspace*{1em}} % Formatting of numbered sections of this type
	{} % Formatting of numberless sections of this type
	{\ \titlerule*[.5pc]{.}\thecontentspage} % Formatting of the filler to the right of the heading and the page number

%% Table text styling
%\titlecontents{table}
%	[1.25cm] % Left indentation
%	{\addvspace{1pt}\sffamily} % Spacing and font options for tables
%	{\thecontentslabel\hspace*{1em}} % Formatting of numbered sections of this type
%	{} % Formatting of numberless sections of this type
%	{\ \titlerule*[.5pc]{.}\;\thecontentspage} % Formatting of the filler to the right of the heading and the page number

%----------------------------------------------------------------------------------------
%	HEADERS AND FOOTERS

\usepackage{fancyhdr} % Required for header and footer configuration
\pagestyle{fancy} % Enable the custom headers and footers

\renewcommand{\chaptermark}[1]{\markboth{\sffamily\normalsize\bfseries\chaptername\ \thechapter.\ #1}{}} % Styling for the current chapter in the header
\renewcommand{\sectionmark}[1]{\markright{\sffamily\normalsize\thesection\hspace{5pt}#1}{}} % Styling for the current section in the header

\fancyhf{} % Clear default headers and footers
\renewcommand{\headrulewidth}{0.5pt} % Thickness of the rule under the header

\fancypagestyle{plain}{% Style for when a plain pagestyle is specified
	\fancyhead{}\renewcommand{\headrulewidth}{0pt}%
}

%----------------------------------------------------------------------------------------
%	Define Variables

\makeatletter
\gdef\@TestName{Test Name}
\def\TestName#1{\gdef\@TestName{#1}}

\gdef\@CompanyName{Company Name}
\def\CompanyName#1{\gdef\@CompanyName{#1}}

\gdef\@CompanyAddr{Company Addr}
\def\CompanyAddr#1{\gdef\@CompanyAddr{#1}}

\gdef\@CompanyIcon{Company Icon}
\def\CompanyIcon#1{\gdef\@CompanyIcon{#1}}

\gdef\@EmployerIcon{Employer Icon}
\def\EmployerIcon#1{\gdef\@EmployerIcon{#1}}
\makeatother

%Header
\makeatletter
\fancyhead[R]{\sffamily\normalsize\thepage}
\fancyhead[C]{\rightmark}
\fancyhead[L]{%
\IfFileExists{\@CompanyIcon}
{\includegraphics[width=5mm,clip,trim={0cm 15mm 0cm 0cm}]{\@CompanyIcon}}
{\fbox{Icon doesn't exist}}%
}
\makeatother

%----------------------------------------------------------------------------------------
%	SECTION NUMBERING IN THE MARGIN

\makeatletter
\renewcommand{\@seccntformat}[1]{\llap{\textcolor{ocre}{\csname the#1\endcsname}\hspace{1em}}}                    
\renewcommand{\section}{\@startsection{section}{1}{\z@}
{-4ex \@plus -1ex \@minus -2.4ex}
{1ex \@plus.2ex }
{\normalfont\Large\sffamily\bfseries}}
\renewcommand{\subsection}{\@startsection {subsection}{2}{\z@}
{-3ex \@plus -0.1ex \@minus -.4ex}
{0.5ex \@plus.2ex }
{\normalfont\large\sffamily\bfseries}}
\renewcommand{\subsubsection}{\@startsection {subsubsection}{3}{\z@}
{-2ex \@plus -0.1ex \@minus -.2ex}
{.2ex \@plus.2ex }
{\normalfont\small\sffamily\bfseries}}                        
\renewcommand\paragraph{\@startsection{paragraph}{4}{\z@}
{-2ex \@plus-.2ex \@minus .2ex}
{.1ex}
{\normalfont\small\sffamily\bfseries}}

%After the above lines
\usepackage{titlesec}
\titlespacing*{\section}
{30pt}{2.5ex plus 1ex minus .2ex}{3.3ex plus .2ex}
\titlespacing*{\subsection}
{37pt}{2.5ex plus 1ex minus .2ex}{3.3ex plus .2ex}


%----------------------------------------------------------------------------------------
%	CHAPTER HEADINGS

% A switch to conditionally include a picture, implemented by Christian Hupfer
\newif\ifusechapterimage
\usechapterimagetrue
\newcommand{\thechapterimage}{}%
\newcommand{\chapterimage}[1]{\ifusechapterimage\renewcommand{\thechapterimage}{#1}\fi}%
\newcommand{\autodot}{.}
\def\@makechapterhead#1{%
{\parindent \z@ \raggedright \normalfont
\ifnum \c@secnumdepth >\m@ne
\if@mainmatter
\begin{tikzpicture}[remember picture,overlay]
\node at (current page.north west)
{\begin{tikzpicture}[remember picture,overlay]
\node[anchor=north west,inner sep=0pt] at (0,0) {\ifusechapterimage\includegraphics[width=\paperwidth]{\thechapterimage}\fi};
\draw[anchor=west] (\Gm@lmargin,-9cm) node [line width=2pt,rounded corners=15pt,draw=ocre,fill=white,fill opacity=0.5,inner sep=15pt]{\strut\makebox[22cm]{}};
\draw[anchor=west] (\Gm@lmargin+.3cm,-9cm) node {\huge\sffamily\bfseries\color{black}\thechapter\autodot~#1\strut};
\end{tikzpicture}};
\end{tikzpicture}
\else
\begin{tikzpicture}[remember picture,overlay]
\node at (current page.north west)
{\begin{tikzpicture}[remember picture,overlay]
\node[anchor=north west,inner sep=0pt] at (0,0) {\ifusechapterimage\includegraphics[width=\paperwidth]{\thechapterimage}\fi};
\draw[anchor=west] (\Gm@lmargin,-9cm) node [line width=2pt,rounded corners=15pt,draw=ocre,fill=white,fill opacity=0.5,inner sep=15pt]{\strut\makebox[22cm]{}};
\draw[anchor=west] (\Gm@lmargin+.3cm,-9cm) node {\huge\sffamily\bfseries\color{black}#1\strut};
\end{tikzpicture}};
\end{tikzpicture}
\fi\fi\par\vspace*{270\p@}}}


\def\@makeschapterhead#1{%
\begin{tikzpicture}[remember picture,overlay]
\node at (current page.north west)
{\begin{tikzpicture}[remember picture,overlay]
\node[anchor=north west,inner sep=0pt] at (0,0) {\ifusechapterimage\includegraphics[width=\paperwidth]{\thechapterimage}\fi};
\draw[anchor=west] (\Gm@lmargin,-9cm) node [line width=2pt,rounded corners=15pt,draw=ocre,fill=white,fill opacity=0.5,inner sep=15pt]{\strut\makebox[22cm]{}};
\draw[anchor=west] (\Gm@lmargin+.3cm,-9cm) node {\huge\sffamily\bfseries\color{black}#1\strut};
\end{tikzpicture}};
\end{tikzpicture}
\par\vspace*{270\p@}}
\makeatother

%----------------------------------------------------------------------------------------
%	LINKS

\usepackage{hyperref}
\hypersetup{hidelinks,colorlinks=false,breaklinks=true,urlcolor=ocre,bookmarksopen=false}

\usepackage{bookmark}
\bookmarksetup{
open,
numbered,
addtohook={%
\ifnum\bookmarkget{level}=0 % chapter
\bookmarksetup{bold}%
\fi
\ifnum\bookmarkget{level}=-1 % part
\bookmarksetup{color=ocre,bold}%
\fi
}}

%----------------------------------------------------------------------------------------
%	Other

\setcounter{secnumdepth}{2}
\renewcommand{\baselinestretch}{1.4}

\setlength{\abovecaptionskip}{0pt plus 1pt minus 2pt}
% For Adding an image
\newcommand\cincludegraphics[2][]{\raisebox{-0.3\height}{\includegraphics[#1]{#2}}}

%----------------------------------------------------------------------------------------
%Some preCommand
 \newsavebox\ltmcbox
\newcommand{\LongTable}[2]{%
\begin{table}[H]
\caption{#2}
\end{table}
 \setbox\ltmcbox\vbox{\hsize=\dimexpr0.5\textwidth-0.5\columnsep
\large
\input{#1}
\unskip
\unpenalty
\unpenalty}
\begin{multicols}{2}
\unvbox\ltmcbox
\end{multicols}
}

%	Define Some Commands
\newcommand{\AddTableO}[2]{%
	\IfFileExists{./table/#1.tex}{%
\begin{minipage}{\linewidth}\centering
	\begin{table}[H]\caption{#2}\vskip -7mm\end{table}
	\input{./table/#1.tex}
	\end{minipage}
	}{}%
}

%	Define Some Commands
\newcommand{\AddTableOMultiPage}[2]{%
	\IfFileExists{./table/#1.tex}{%
	\begin{table}[H]\caption{#2}\vskip -7mm\end{table}
	\input{./table/#1.tex}
	}{}%
}

\newcommand{\AddTableOO}[2]{%
	\IfFileExists{./table/#1.tex}{%
\begin{minipage}{0.45\linewidth}\centering
	\begin{table}[H]\caption{#2}\vskip -7mm\end{table}
	\input{./table/#1.tex}
	\end{minipage}
	}{}%
}

\newcommand{\AddLegendO}[2]{%
	\IfFileExists{./legend/#1}{%
\begin{minipage}{\linewidth}\centering
	\begin{table}[H]\caption{#2}\vskip -7mm\end{table}
	\input{./legend/#1}
	\end{minipage}
	}{}%
}

\newcommand{\AddMapAllLeg}[2]{%
\IfFileExists{./pic/#1.png}{%
\clearpage
\vfill
\begin{figure}\centering
\caption{#2}
\vskip 5mm
\begin{tikzpicture}
\node [](P){\includegraphics[width=0.66\linewidth]{./pic/#1.png}};
\IfFileExists{./static/#1.tex}{%
\node at(P.south west)[below right,shape=rectangle,fill=yellow,rounded corners=2mm](Q){Statitic Information};
\node at(Q.south west)[below right,shape=rectangle,fill=white](R){\input{./static/#1.tex}};
}{%
\node at(P.north east)[below right](R){};
}%
\IfFileExists{./legend/#1.tex}{%
\node at(P.north east)[below right,shape=rectangle,fill=yellow,rounded corners=2mm,yshift=-2mm](S){Color Information};
\node at(S.south west)[below right,shape=rectangle,fill=white](T){\input{./legend/#1.tex}};
}{%
\node at(P.north east)[below right](T){};
}%
\IfFileExists{./info/#1.tex}{%
\node at(T.south west)[below right,shape=rectangle,fill=yellow,rounded corners=2mm,yshift=-2mm](U){Ranges};
\node at(U.south west)[below right,shape=rectangle,fill=white](V){\input{./info/#1.tex}};
}{}%
\end{tikzpicture}
\end{figure}
\vfill%
}{}%
}

\newcommand{\AddMapAllLegInfoOut}[2]{%
\IfFileExists{./pic/#1.png}{%
\clearpage
\vfill
\begin{figure}\centering
\caption{#2}
\vskip 5mm
\begin{tikzpicture}
\node [](P){\includegraphics[width=0.67\linewidth]{./pic/#1.png}};
\IfFileExists{./static/#1.tex}{%
\node at(P.south west)[below right,shape=rectangle,fill=yellow,rounded corners=2mm](Q){Statitic Information};
\node at(Q.south west)[below right,shape=rectangle,fill=white](R){\input{./static/#1.tex}};
}{%
\node at(P.north east)[below right](R){};
}%
\IfFileExists{./legend/#1.tex}{%
\node at(P.north east)[below right,shape=rectangle,fill=yellow,rounded corners=2mm,yshift=-2mm](S){Color Information};
\node at(S.south west)[below right,shape=rectangle,fill=white](T){\input{./legend/#1.tex}};
}{%
\node at(P.north east)[below right](T){};
}%
\end{tikzpicture}
\end{figure}
\vfill%
\clearpage
\IfFileExists{./info/#1.tex}{\LongTable{./info/#1.tex}{#2}}{}
}{}%
}

\newcommand{\AddMapLegO}[2]{%
\IfFileExists{./pic/#1.png}{%
\vfill
\begin{figure}
\centering
\includegraphics[height=0.98\textheight]{./pic/#1}
\caption{#2}
\end{figure}
\vfill
}{}
\IfFileExists{./legend/#1.tex}{%
\clearpage
\begin{table}[H]\caption{#2}\vskip -7mm\end{table}
\input{./legend/#1.tex}
}{}
}

\newcommand{\AddPicLegOO}[2]{%
\IfFileExists{./pic/#1.png}{%
\vfill
\begin{figure}
\centering
\includegraphics[height=0.98\textheight]{./pic/#1}
\caption{#2}
\end{figure}
\vfill
}{}
\IfFileExists{./legend/#1.tex}{%
\clearpage
\LongTable{./legend/#1.tex}{#2}
}{}
}

\newcommand{\AddMapNoLeg}[3][png]{%
\IfFileExists{./pic/#2.#1}{%
\clearpage
\vfill
\begin{figure}\centering
\includegraphics[height=0.98\textheight,keepaspectratio]{./pic/#2};
\caption{#3}
\end{figure}
\vfill%
}{}%
}

\newcommand{\AddPicNoLegend}[3][0.98]{%
\IfFileExists{./pic/#2}{%
\clearpage
\vfill
\begin{figure}\centering
\includegraphics[height=#1\textheight,keepaspectratio]{./pic/#2};
\caption{#3}
\end{figure}
\vfill%
}{}%
}

\newcommand{\AddMapLegOut}[2]{%
\IfFileExists{./pic/#1.png}{%
\clearpage
\vfill
\begin{figure}
\centering
\begin{subfigure}[b]{0.62\textwidth}\centering
\includegraphics[width=0.95\linewidth]{./pic/#1}
\end{subfigure}
\begin{subfigure}[b]{0.23\textwidth}\centering\large
\input{./legend/#1.tex}
\end{subfigure}
\caption{#2}
\end{figure}
\vfill
}{}
}

\newcommand{\AddPicLegOut}[2]{%
	\IfFileExists{./pic/#1.pdf}{%
		\IfFileExists{./legend/#1.tex}{%
		\clearpage
		\vfill
		\begin{figure}
		\centering
		\begin{subfigure}[b]{0.68\textwidth}\centering
		\includegraphics[width=\linewidth]{./pic/#1}
		\end{subfigure}
		\begin{subfigure}[b]{0.29\textwidth}\centering\large
		\input{./legend/#1.tex}
		\end{subfigure}
		\caption{#2}
		\end{figure}
		\vfill
		}{}
	}{}
}


\newcommand{\AddPicLegOutG}[2]{%
\IfFileExists{./pic/#1.pdf}{%
\clearpage
\vfill
\begin{figure}\centering

\begin{tikzpicture}
\node [](P){\includegraphics[width=0.67\linewidth]{./pic/#1.pdf}};
\IfFileExists{./legend/#1.tex}{%
\node at(P.north east)[below right,shape=rectangle,fill=yellow,rounded corners=2mm](Q){Legend};
\node at(Q.south west)[below right,shape=rectangle,fill=white,scale=1.1](R){\input{./legend/#1.tex}};
}{%
\node at(P.north east)[below right](R){};
}%
\end{tikzpicture}
\caption{#2}
\end{figure}
\vfill%
}{}%
}
