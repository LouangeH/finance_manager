from django.urls import path
from app.views import user, accueil, revenue, depense,bank, cat_bank, cat_depense, cat_revenue
from app.views import generate_pdf

urlpatterns = [
    path('', accueil.dashboard, name='dashboard'),

    path('revenues/', revenue.revenue_list, name='revenue_list'),
    path('revenu/<int:revenu_id>/pdf/', generate_pdf.revenu_pdf_view, name='revenu_pdf'),
    path('ajouter-revenue/', revenue.create_revenue, name='create_revenue'),
    path('modifier-revenue/<int:pk>/', revenue.edit_revenue, name='edit_revenue'),
    path('supprimer-revenue/<int:pk>/', revenue.delete_revenue, name='delete_revenue'),
    
    path('cat-revenues/', cat_revenue.cat_revenue_list, name='cat_revenue_list'),
    path('ajouter-cat-revenue/', cat_revenue.create_cat_revenue, name='create_cat_revenue'),
    path('modifier-cat-revenue/<int:pk>/', cat_revenue.update_cat_revenue, name='update_cat_revenue'),
    path('supprimer-cat-revenue/<int:pk>/', cat_revenue.delete_cat_revenue, name='delete_cat_revenue'),

    path('cat-depenses/', cat_depense.cat_depense_list, name='cat_depense_list'),
    path('ajouter-cat-depense/', cat_depense.create_cat_depense, name='create_cat_depense'),
    path('modifier-cat-depense/<int:pk>/', cat_depense.update_cat_depense, name='update_cat_depense'),
    path('supprimer-cat-depense/<int:pk>/', cat_depense.delete_cat_depense, name='delete_cat_depense'),

    path('depenses/', depense.depense_list, name='depense_list'),
    path('depense/<int:depense_id>/pdf/', generate_pdf.depense_pdf_view, name='depense_pdf'),
    path('ajouter-depense/', depense.create_depense, name='create_depense'),
    path('modifier-depense/<int:pk>/', depense.edit_depense, name='edit_depense'),
    path('supprimer-depense/<int:pk>/', depense.delete_depense, name='delete_depense'),

    path('login/', user.login_view, name='login'),
    path('register/', user.register_view, name='register'),
    path('logout/', user.logout_view, name='logout'),
    path('user/', user.user_list, name='user_list'),
    path('modifier-user/<int:pk>/', user.edit_user, name='update_user'),
    path('supprimer-user/<int:pk>/', user.delete_user, name='delete_user'),

    path('cat-banks/', cat_bank.bank_list, name='bank_list'),
    path('ajouter-cat-bank/', cat_bank.create_bank, name='create_bank'),
    path('modifier-cat-bank/<int:pk>/', cat_bank.update_bank, name='update_bank'),
    path('supprimer-cat-bank/<int:pk>/', cat_bank.delete_bank, name='delete_bank'),

    path('banque/', bank.bank_operation_list, name='bankoperation_list'),
    path('banque/ajouter/', bank.create_bank_operation, name='bankoperation_create'),
    path('api/solde-banque/<int:bank_id>/', bank.get_bank_solde, name='get_bank_solde'),
    path('banque/modifier/<int:pk>/', bank.update_bank_operation, name='bankoperation_update'),
    path('banque/supprimer/<int:pk>/', bank.delete_bank_operation, name='bankoperation_delete'),
]