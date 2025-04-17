"""
* Zibal Payment Test Task
*
* Developer: Ali Sharifi
* Email: alisharifyofficial@gmail.com
* Website: ali-sharify.ir
* GitHub: github.com/alisharify7/zibal
* Repository: https://github.com/alisharify7/zibal
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.TransactionView.as_view(), name="transaction"),
    path("cache/", views.TransactionView.as_view(), name="cached-transaction"),
]
