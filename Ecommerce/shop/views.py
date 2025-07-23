from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Product, Commande
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib import messages
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import ContactForm

def index(request): 
    product_object = Product.objects.all()
    item_name = request.GET.get('item-name')
    
    if item_name and item_name.strip() != '':
        product_object = Product.objects.filter(title__icontains=item_name)
    
    paginator = Paginator(product_object, 4)  
    page = request.GET.get('page')
    product_object = paginator.get_page(page)
    return render(request, 'shop/index.html', {'product_object': product_object})

def detail(request, myid):
    product = get_object_or_404(Product, id=myid)
    return render(request, 'shop/detail.html', {'product': product})

def checkout(request):
    if request.method == "POST":
        try:
            panier_json = request.POST.get('items')
            panier_data = json.loads(panier_json) if panier_json else {}
        except json.JSONDecodeError:
            return render(request, 'shop/checkout.html', {
                'error': "Erreur lors de l'analyse du panier."
            })

        nom = request.POST.get('nom')
        email = request.POST.get('email')
        address = request.POST.get('address')
        ville = request.POST.get('ville')
        pays = request.POST.get('pays')
        zipcode = request.POST.get('zipcode')
        
        if not all([nom, email, address, ville, pays, zipcode]):
            return render(request, 'shop/checkout.html', {
                'error': 'Tous les champs sont obligatoires'
            })

        items = []
        for product_id, item in panier_data.items():
            try:
                product = Product.objects.get(id=int(product_id))
                quantity = int(item.get('quantity', 1))
                items.append(f"{product.title} ({quantity})")
            except (Product.DoesNotExist, ValueError):
                continue

        if not items:
            return render(request, 'shop/checkout.html', {
                'error': "Le panier est vide ou contient des produits invalides."
            })

        com = Commande(
            items=", ".join(items),
            nom=nom,
            email=email,
            address=address,
            ville=ville,
            pays=pays,
            zipcode=zipcode
        )
        com.save()

        return redirect('confirmation')

    return render(request, 'shop/checkout.html')

def confirmation(request):
    return render(request, 'shop/confirmation.html')

@login_required
@require_POST
def add_to_cart(request, product_id):
    # Récupère le produit ou renvoie 404 si non trouvé
    product = get_object_or_404(Product, id=product_id)
    
    # Récupère la quantité (avec valeur par défaut 1)
    quantity = int(request.POST.get('quantity', 1))
    
    # Ici vous devriez implémenter votre logique de panier
    # Par exemple, en utilisant la session Django :
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    request.session['cart'] = cart
    
    # Message de confirmation
    messages.success(request, f"{product.title} a été ajouté à votre panier")
    
    # Redirection vers la page précédente avec paramètre anti-cache
    referer = request.META.get('HTTP_REFERER', '/')
    if '?' in referer:
        return redirect(f"{referer}&t={time.time()}")
    else:
        return redirect(f"{referer}?t={time.time()}")
    

# Connexion
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # change 'home' selon ta page d'accueil
        else:
            return render(request, 'shop/login.html', {'error': "Identifiants invalides."})
    return render(request, 'shop/login.html')


# Inscription
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'shop/register.html', {'error': "Les mots de passe ne correspondent pas."})

        if User.objects.filter(username=username).exists():
            return render(request, 'shop/register.html', {'error': "Nom d'utilisateur déjà utilisé."})

        if User.objects.filter(email=email).exists():
            return render(request, 'shop/register.html', {'error': "Email déjà utilisé."})

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('home')  # change 'home' selon ta page d'accueil

    return render(request, 'shop/register.html')


# Déconnexion
def logout_view(request):
    logout(request)
    return redirect('login')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Données extraites
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Préparer l'email
            full_message = f"Message de : {name} <{email}>\n\n{message}"
            try:
                send_mail(subject, full_message, email, ['contact@premiumshop.com'])  # à modifier avec ton email
                messages.success(request, "Votre message a bien été envoyé.")
                return redirect('contact')
            except Exception as e:
                messages.error(request, "Une erreur est survenue lors de l'envoi.")
    else:
        form = ContactForm()

    return render(request, 'shop/contact.html', {'form': form})


from django.http import HttpResponse

def about_view(request):
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        email = request.POST['newsletter_email']
        # Gérer l'inscription à la newsletter (enregistrement dans une base de données ou envoi d'email)
        return HttpResponse("Merci pour votre abonnement à notre newsletter!", status=200)
    
    return render(request, 'shop/about.html')


    
