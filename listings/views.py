from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Listing
from .choices import bedroom_choices, price_choices, state_choices


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    page_listings = paginator.get_page(page)

    return render(request, 'listings/listings.html', {
        'listings': page_listings
    })


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing
    }
    return render(request, 'listings/listing.html', context=context)


def search(request):
    queryset_listings = Listing.objects.order_by('-list_date')

    # Keywords

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_listings = queryset_listings.filter(
                description__icontains=keywords)

    # City

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_listings = queryset_listings.filter(
                city__iexact=city)

    # State

    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_listings = queryset_listings.filter(
                state__iexact=state)

    # Bedrooms

    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_listings = queryset_listings.filter(
                bedrooms__lte=bedrooms)

    # Max price

    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_listings = queryset_listings.filter(
                price__lte=price)
    context = {
        'price_choices': price_choices,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'listings': queryset_listings,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context=context)
