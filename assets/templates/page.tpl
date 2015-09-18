<!DOCTYPE html>
<html>
<head lang="ru">
    <meta charset="UTF-8">
    <base href="${base_url}">

    <title>${title}</title>

    <link rel="stylesheet" href="assets/styles/reset.css"/>
    <link rel="stylesheet" href="assets/styles/page.css"/>
    <link rel="stylesheet" href="assets/styles/main.css"/>
    <link rel="stylesheet" href="assets/styles/comment.css"/>
    <link rel="stylesheet" href="assets/styles/stat.css"/>
    <link rel="stylesheet" href="assets/styles/view.css"/>

    <script src="assets/scripts/page.js"></script>
    <script src="assets/scripts/main.js"></script>
    <script src="assets/scripts/comment.js"></script>
    <script src="assets/scripts/view.js"></script>
</head>
<body>
<div class="page-wrapper">
    <aside class="info-tip"></aside>
    <main class="main">
        <a href="/">
            <header class="main-header">
                ${main_header}
            </header>
        </a>
    </main>
    <section class="main-section">
        ${main_section}
    </section>
    </main>
</div>
</body>
</html>