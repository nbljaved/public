;;; publish.el --- Blog publishing configuration for nbljaved.com

;; TODO: tags
;; TODO: Which books I have read in my about section.
;; TODO: A notes section, there are some articles that I like


;; Set up package installation directory so that packages aren't stored in
;; ~/.emacs.d/elpa path.
(require 'package)
(setq package-user-dir (expand-file-name "./.packages"))
(setq package-archives '(("elpa" . "https://elpa.gnu.org/packages/")
                         ("melpa" . "https://melpa.org/packages/")))

;; Initialize the package system
(package-initialize)
(unless package-archive-contents
  (package-refresh-contents))

;; Install use-package
(unless (package-installed-p 'use-package)
  (package-install 'use-package))
(require 'use-package)
(require 'use-package-ensure)
(setq use-package-always-ensure t)

(require 'ox-publish)
(require 'ox-html)

;; Export to HTML with useful anchors
;; Modified from: https://github.com/alphapapa/unpackaged.el#export-to-html-with-useful-anchors
(require 'easy-mmode)
(require 'ox)
(require 'dash)

(use-package ox
  :ensure nil
  :config
  (define-minor-mode unpackaged/org-export-html-with-useful-ids-mode
    "Attempt to export Org as HTML with useful link IDs.
Instead of random IDs like \"#orga1b2c3\", use heading titles,
made unique when necessary."
    :global t
    (if unpackaged/org-export-html-with-useful-ids-mode
        (advice-add #'org-export-get-reference :override #'unpackaged/org-export-get-reference)
      (advice-remove #'org-export-get-reference #'unpackaged/org-export-get-reference)))

  (defun unpackaged/org-export-get-reference (datum info)
    "Like `org-export-get-reference', except uses heading titles instead of random numbers."
    (let ((cache (plist-get info :internal-references)))
      (or (car (rassq datum cache))
          (let* ((crossrefs (plist-get info :crossrefs))
                 (cells (org-export-search-cells datum))
                 ;; Preserve any pre-existing association between
                 ;; a search cell and a reference, i.e., when some
                 ;; previously published document referenced a location
                 ;; within current file (see
                 ;; `org-publish-resolve-external-link').
                 ;;
                 ;; However, there is no guarantee that search cells are
                 ;; unique, e.g., there might be duplicate custom ID or
                 ;; two headings with the same title in the file.
                 ;;
                 ;; As a consequence, before re-using any reference to
                 ;; an element or object, we check that it doesn't refer
                 ;; to a previous element or object.
                 (new (or (cl-some
                           (lambda (cell)
                             (let ((stored (cdr (assoc cell crossrefs))))
                               (when stored
                                 (let ((old (org-export-format-reference stored)))
                                   (and (not (assoc old cache)) stored)))))
                           cells)
                          (when (org-element-property :raw-value datum)
                            ;; Heading with a title
                            (unpackaged/org-export-new-title-reference datum cache))
                          ;; NOTE: This probably breaks some Org Export
                          ;; feature, but if it does what I need, fine.
                          (org-export-format-reference
                           (org-export-new-reference cache))))
                 (reference-string new))
            ;; Cache contains both data already associated to
            ;; a reference and in-use internal references, so as to make
            ;; unique references.
            (dolist (cell cells) (push (cons cell new) cache))
            ;; Retain a direct association between reference string and
            ;; DATUM since (1) not every object or element can be given
            ;; a search cell (2) it permits quick lookup.
            (push (cons reference-string datum) cache)
            (plist-put info :internal-references cache)
            reference-string))))

  (defun unpackaged/org-export-new-title-reference (datum cache)
    "Return new reference for DATUM that is unique in CACHE."
    (cl-macrolet ((inc-suffixf (place)
                    `(progn
                       (string-match (rx bos
                                         (minimal-match (group (1+ anything)))
                                         (optional "--" (group (1+ digit)))
                                         eos)
                                     ,place)
                       ;; HACK: `s1' instead of a gensym.
                       (-let* (((s1 suffix) (list (match-string 1 ,place)
                                                  (match-string 2 ,place)))
                               (suffix (if suffix
                                           (string-to-number suffix)
                                         0)))
                         (setf ,place (format "%s--%s" s1 (cl-incf suffix)))))))
      (let* ((title (org-element-property :raw-value datum))
             (ref (url-hexify-string (substring-no-properties title)))
             (parent (org-element-property :parent datum)))
        (while (--any (equal ref (car it))
                      cache)
          ;; Title not unique: make it so.
          (if parent
              ;; Append ancestor title.
              (setf title (concat (org-element-property :raw-value parent)
                                  "--" title)
                    ref (url-hexify-string (substring-no-properties title))
                    parent (org-element-property :parent parent))
            ;; No more ancestors: add and increment a number.
            (inc-suffixf ref)))
        ref))))

;; Install dependencies
(use-package htmlize
  :pin elpa
  :custom
  ;; see Readme.org in this folder about code highlighting
  (org-html-htmlize-output-type 'css))

(use-package webfeeder
  :pin elpa)

;; https://github.com/tali713/esxml
(use-package esxml)
(require 'esxml)

(setq org-html-validation-link nil
      org-html-head-include-scripts nil       ;; we will set our own
      org-html-head-include-default-style nil ;; we will set our own
      ;; https://github.com/kevquirk/simple.css/wiki/Getting-Started-With-Simple.css
      org-html-head (concat
                     ;; Cannot wrap this in a div, as that would put these links inside the 'body'
                     ;; instead of the 'head'.
                     (esxml-to-xml `(link ((rel . "stylesheet")
                                           (href . "/static/css/simple.css"))))
                     (esxml-to-xml `(link ((rel . "stylesheet")
                                           (href . "/static/css/custom.css"))))
                     (esxml-to-xml `(link ((rel . "stylesheet")
                                           (href . "/static/css/highlight.css"))))
                     (esxml-to-xml `(link ((rel . "icon")
                                           (type . "image/svg+xml")
                                           (href . "/static/img/nj.svg")))))
      org-html-divs '((preamble "header" "preamble")
                      (content "main" "content")
                      (postamble "footer" "postamble"))
      ;; org-html-container-element "section"
      ;; org-html-metadata-timestamp-format "%Y-%m-%d"
      ;; org-html-checkbox-type 'html
      ;;
      ;; https://www.gnu.org/software/emacs/manual/html_node/org/HTML-doctypes.html
      ;; HTML5 documents can have arbitrary ‘#+BEGIN’ … ‘#+END’ blocks When
      ;; Special blocks do not have a corresponding HTML5 element, the HTML
      ;; exporter reverts to standard translation (see
      ;; org-html-html5-elements). For example, ‘#+BEGIN_lederhosen’ exports to
      ;; <div class="lederhosen">.
      ;;
      ;; https://www.gnu.org/software/emacs/manual/html_node/org/HTML-Export.html
      ;; https://www.gnu.org/software/emacs/manual/html_node/org/Quoting-HTML-tags.html
      ;;
      ;; Also see Macro replacement: https://orgmode.org/manual/Macro-Replacement.html
      ;;
      org-html-doctype "html5"
      org-html-html5-fancy t
      org-html-self-link-headlines nil)

(defun org-blog-timestamp (arg1)
  "Generate HTML timestamp div for blog posts.
   ARG1 is an optional last-updated date string. When provided and non-empty,
   it displays 'Last updated: ARG1' below the publication date."
  (concat "@@html:<div class=\"timestamp2\">@@"
          "@@html:<div hidden class=\"published\">@@"
          "{{{date(%Y-%m-%d)}}}"
          "@@html:</div>@@"
          ;;
          "@@html:<div>@@"
          "{{{date(%B %d\\, %Y)}}}"
          "@@html:</div>@@"
          "@@html:<i>@@"
          (when (and arg1 (not (string-empty-p arg1)))
            (concat "@@html:<div>@@"
                    "Last updated: "
                    arg1
                    "@@html:</div>@@"))
          "@@html:</i>@@"
          ;;
          "@@html:</div>@@"))

(setq org-export-global-macros
      '(("timestamp" . "@@html:<span class=\"timestamp\">$1</span>@@")
        ("published" . "(eval (org-blog-timestamp $1))")))

(defun org-blog-sitemap-format-entry (entry style project)
  "Format sitemap entries for blog posts.
   We modified org-publish-sitemap-default-entry

   Default format for site map ENTRY, as a string.
   ENTRY is a file name.  STYLE is style of sitemap.
   PROJECT is the current project."
  (cond ((not (directory-name-p entry))
         (format "{{{timestamp(%s)}}} [[file:%s][%s]]"
                 (format-time-string "%Y %b %d" (org-publish-find-date entry project))
                 entry
                 (org-publish-find-title entry project)))
	((eq style 'tree)
	 ;; Return only last subdir.
	 (file-name-nondirectory (directory-file-name entry)))
	(t entry)))

(defun org-blog-sitemap-function (title list)
  "Generate sitemap for blog posts."
  (concat "#+TITLE: " title "\n\n"
          (format "#+begin_export html\n\n%s \n \n#+end_export \n\n"
                  (esxml-to-xml
                   `(div ((class . "atom-feed"))
                         (a ((href . "/blog/atom.xml"))
                            "Atom Feed "
                            (img ((src . "/static/img/feed-icon.svg")
                                  (class . "feed-icon")))))))
          (org-list-to-org list)))

(defun nbljaved.com/header ()
  (esxml-to-xml
   `(div ()
         (h1 () "Nabeel Javed")
         (nav ()
              (a ((href . "/")) "Blog")
              (a ((href . "/about.html")) "About")))))

(defun nbljaved.com/footer ()
  (concat
   (esxml-to-xml
    `(div ()
          "Created with "
          (a ((href . "https://www.gnu.org/software/emacs/"))
             (img ((src . "/static/img/EmacsIcon.svg")
                   (style . "height:1.2em;position:relative;top:0.25em"))))
          " and "
          (a ((href . "https://orgmode.org/"))
             (img ((src . "/static/img/Org-mode-unicorn.svg")
                   (style . "height:1.2em;position:relative;top:0.25em"))))
          (div ((class . "source-link"))
               (a ((href . "https://github.com/nbljaved/public/tree/main/nbljaved.com"))
                  "Source code for this site"))
          (comment () "Cloudflare Web Analytics")
          (script ((defer . "") ;  <script defer=""> is the same as <script defer>
                   (src . "https://static.cloudflareinsights.com/beacon.min.js")
                   (data-cd-beacon . "{\"token\": \"21afbb500f704e30849cbe64ad813cf1\"}"))
                  "")
          (comment () "End Cloudflare Web Analytics")))))

(setq org-publish-project-alist
      `(("nbljaved"
         :components ("blog" "blog-static" "static" "pages"))
        ("blog"
         :base-directory ,(expand-file-name "org/blog" (file-name-directory (or load-file-name buffer-file-name)))
         :base-extension "org"
         :exclude "draft\.org$"
         :publishing-directory ,(expand-file-name "html/blog" (file-name-directory (or load-file-name buffer-file-name)))
         :publishing-function org-html-publish-to-html
         :headline-levels 4
         :html-preamble ,(nbljaved.com/header)
         :html-postamble ,(nbljaved.com/footer)
         :with-toc nil
         :section-numbers t
         :with-author nil             ; Don't include author name
         :with-creator t              ; Include Emacs and Org versions in footer
         :time-stamp-file nil         ; Don't include time stamp in file
         :auto-sitemap t
         :sitemap-filename "index.org"
         :sitemap-title ""   ;; "Blog Posts"
         :sitemap-style list ; defaults to - tree, can set to - list
         :sitemap-sort-files anti-chronologically
         :sitemap-format-entry org-blog-sitemap-format-entry
         :sitemap-function org-blog-sitemap-function
         :recursive t)
        ("blog-static"
         :base-directory ,(expand-file-name "org/blog" (file-name-directory (or load-file-name buffer-file-name)))
         :base-extension "css\\|js\\|svg\\|png\\|jpg\\|gif\\|pdf\\|mp3\\|ogg\\|swf\\|txt"
         :publishing-directory ,(expand-file-name "html/blog" (file-name-directory (or load-file-name buffer-file-name)))
         :publishing-function org-publish-attachment
         :recursive t)
        ("pages"
         :base-directory ,(expand-file-name "org" (file-name-directory (or load-file-name buffer-file-name)))
         :base-extension "org"
         :exclude "^blog/.*"
         :publishing-directory ,(expand-file-name "html" (file-name-directory (or load-file-name buffer-file-name)))
         :publishing-function org-html-publish-to-html
         :headline-levels 4
         :html-preamble ,(nbljaved.com/header)
         :html-postamble ,(nbljaved.com/footer)
         :with-toc t
         :section-numbers nil
         :with-author nil             ; Don't include author name
         :with-creator t              ; Include Emacs and Org versions in footer
         :time-stamp-file nil         ; Don't include time stamp in file
         )
        ("static"
         :base-directory ,(expand-file-name "org/static" (file-name-directory (or load-file-name buffer-file-name)))
         :base-extension "css\\|js\\|svg\\|png\\|jpg\\|gif\\|pdf\\|mp3\\|ogg\\|swf\\|txt"
         :publishing-directory ,(expand-file-name "html/static" (file-name-directory (or load-file-name buffer-file-name)))
         :publishing-function org-publish-attachment
         :recursive t)))

(defun atom-extract-title (html-file)
  "Extract the title from an HTML file."
  (with-temp-buffer
    (insert-file-contents html-file)
    (let* ((dom (libxml-parse-html-region (point-min) (point-max)))
           (title (dom-text (car (dom-by-class dom "title")))))
      (if (or (not title) (string= "" title))
          (error (format "Title doesn't exist in filename: %s" html-file))
        title))))

(defun atom-extract-date (html-file)
  "Extract the date from an HTML file."
  (with-temp-buffer
    (insert-file-contents html-file)
    (let* ((dom (libxml-parse-html-region (point-min) (point-max)))
           (date (dom-text (car (dom-by-class dom "published")))))

      (if (or (not date) (string= "" date))
          (error (format "Date doesn't exist in filename: %s" html-file))
        (let* ((parsed-date (parse-time-string date))
               (day (nth 3 parsed-date))
               (month (nth 4 parsed-date))
               (year (nth 5 parsed-date)))
          ;; NOTE: Hardcoding this at 8am for now
          (encode-time 0 0 8 day month year))))))

;; https://gitlab.com/ambrevar/emacs-webfeeder
(defun nbljaved.com/generate-feed ()
  "Generate Atom feed from published blog posts."
  (let* ((project-dir (expand-file-name "html/blog" (file-name-directory (or load-file-name buffer-file-name))))
         (posts-dir (expand-file-name "posts" project-dir))
         (url "https://nbljaved.com/blog/")
         ;; Get relative paths from project-dir (webfeeder expects paths relative to project-dir)
         (html-files (mapcar (lambda (f) (concat "posts/" f))
                             (directory-files posts-dir nil "\\.html$"))))
    (let ((webfeeder-title-function #'atom-extract-title)
          (webfeeder-date-function #'atom-extract-date))
      (webfeeder-build
       "atom.xml"
       project-dir
       url
       html-files
       :title "Nabeel Javed's Blog"
       :description "Nabeel's blog posts feed in Atom"
       :author "Nabeel Javed"
       :max-entries 20))))

(defun nbljaved.com/publish ()
  "Publish entire site"
  (unpackaged/org-export-html-with-useful-ids-mode)
  (org-publish-all t)
  (message "Generating feed...")
  (nbljaved.com/generate-feed)
  (message "Feed successfully generated"))

(nbljaved.com/publish)

(provide 'publish)

;;; publish.el ends here
