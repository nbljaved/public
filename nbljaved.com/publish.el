;;; publish.el --- Blog publishing configuration for nbljaved.com

;; Reference websites:
;; https://taingram.org/blog/org-mode-blog.html
;; https://systemcrafters.net/publishing-websites-with-org-mode/building-the-site/

(require 'ox-publish)
(require 'ox-html)

;; TODO: HTML link home, HTML link up, HTML container,

(setq org-html-validation-link nil
      org-html-head-include-scripts nil       ;; we will set our own
      org-html-head-include-default-style nil ;; we will set our own
      ;; https://github.com/kevquirk/simple.css/wiki/Getting-Started-With-Simple.css
      org-html-head (concat "<link rel=\"stylesheet\" href=\"/static/css/simple.css\" />"
                            "\n"
                            "<link rel=\"stylesheet\" href=\"/static/css/custom.css\" />")
      ;;
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
      org-html-doctype "html5"
      org-html-html5-fancy t
      org-html-self-link-headlines nil)

(defun org-blog-sitemap-format-entry (entry style project)
  "Format sitemap entries for blog posts."
  (format "[[file:%s][%s]]\n%s\n"
          entry
          (org-publish-find-title entry project)
          (format-time-string "%Y-%m-%d" (org-publish-find-date entry project))))

(defun org-blog-sitemap-function (title list)
  "Generate sitemap for blog posts."
  (concat "#+TITLE: Blog\n\n"
          (mapconcat 'identity list "\n")))

(defun nbljaved.com/header ()
  "
  <h1>Nabeel Javed</h1>
  <nav>
  <a href=\"/\">Blog</a>
  <a href=\"/about.html\">About</a>
  </nav>
  ")

(defun nbljaved.com/footer ()
  "
  Created with
    <a href=\"https://www.gnu.org/software/emacs/\">
      <img src=\"/static/img/EmacsIcon.svg\" style=\"height:1.2em;position:relative;top:0.25em\"></a>
    and
    <a href=\"https://orgmode.org/\">
      <img src=\"/static/img/Org-mode-unicorn.svg\" style=\"height:1.2em;position:relative;top:0.25em\">
    </a>
    <!-- Cloudflare Web Analytics -->
    <script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{\"token\": \"21afbb500f704e30849cbe64ad813cf1\"}'></script>
    <!-- End Cloudflare Web Analytics -->
  "
  ;; "hi"
  )

(setq org-publish-project-alist
      `(("nbljaved"
         :components ("blog" "static" "pages"))
        ("blog"
         :base-directory ,(expand-file-name "org/blog" (file-name-directory (or load-file-name buffer-file-name)))
         :base-extension "org"
         :exclude "draft\.org$"
         :publishing-directory ,(expand-file-name "html/blog" (file-name-directory (or load-file-name buffer-file-name)))
         :publishing-function org-html-publish-to-html
         :headline-levels 4
         :html-preamble ,(nbljaved.com/header)
         :html-postamble ,(nbljaved.com/footer)
         :with-toc t
         :section-numbers nil
         :with-author nil             ; Don't include author name
         :with-creator t              ; Include Emacs and Org versions in footer
         :time-stamp-file nil         ; Don't include time stamp in file
         :auto-sitemap t
         :sitemap-filename "index.org"
         :sitemap-title "" ;; "Blog Posts"
         :sitemap-sort-files anti-chronologically
         ;; :sitemap-format-entry org-blog-sitemap-format-entry
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

(provide 'publish)

;;; publish.el ends here
