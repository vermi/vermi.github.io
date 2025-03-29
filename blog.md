---
layout: default
title: Blog
---

# Thoughts & Explorations

I write about technology, security, and whatever else catches my interest.

## Tutorials

{% for post in site.categories.tutorials %}
- [{{ post.title }}]({{ post.url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endfor %}

## Opinions

{% for post in site.categories.opinions %}
- [{{ post.title }}]({{ post.url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endfor %}

## Research

{% for post in site.categories.research %}
- [{{ post.title }}]({{ post.url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endfor %}
