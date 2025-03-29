---
layout: default
title: Blog
---

<div class="blog-layout">
  <!-- Main content - Chronological posts -->
  <div class="main-content">
    <h1>Recent Posts</h1>
    
    <ul class="post-list">
      {% for post in site.posts %}
        <li>
          <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
          <span class="post-date">{{ post.date | date: "%B %d, %Y" }}</span>
          {% if post.description %}
            <p class="post-description">{{ post.description }}</p>
          {% endif %}
        </li>
      {% endfor %}
    </ul>
  </div>

  <!-- Sidebar -->
  <div class="sidebar">
    <div class="sidebar-section">
      <h3>Categories</h3>
      <ul class="category-list">
        {% assign sorted_categories = site.categories | sort %}
        {% for category in sorted_categories %}
          <li>
            <a href="#{{ category[0] | slugify }}">
              {{ category[0] | capitalize }} ({{ category[1].size }})
            </a>
          </li>
        {% endfor %}
      </ul>
    </div>
  </div>
</div>

<div class="category-sections">
  {% for category in site.categories %}
    <div id="{{ category[0] | slugify }}" class="category-section">
      <h2>{{ category[0] | capitalize }}</h2>
      <ul>
        {% for post in category[1] %}
          <li>
            <a href="{{ post.url }}">{{ post.title }}</a> - {{ post.date | date: "%B %d, %Y" }}
          </li>
        {% endfor %}
      </ul>
    </div>
  {% endfor %}
</div>
