#!/usr/bin/python
#coding: utf-8
#(c) 2017 Ramses Carbajal <@RamsesCarbajal>

from . import BaseEndpointTestCase

class OrdersEndpointTestCase(BaseEndpointTestCase):

    def test_01_customer_all(self):
        self.client.api_key = '1tv5yJp3xnVZ7eK67m4h'
        customer1 = self.client.Customer.create(self.customer_object.copy())
        customer2 = self.client.Customer.create(self.customer_object.copy())
        customer3 = self.client.Customer.create(self.customer_object.copy())
        
        customers = self.client.Customer.where()
        assert customers[0].id    

    def test_02_customer_pagination_next(self):
        self.client.api_key = '1tv5yJp3xnVZ7eK67m4h'
        customer1 = self.client.Customer.create(self.customer_object.copy())
        customer2 = self.client.Customer.create(self.customer_object.copy())
        customer3 = self.client.Customer.create(self.customer_object.copy())
        query = {}
        query["next"] = customer1.id
        customers = self.client.Customer.where(query)
        new_search = customers.next()

        custs = new_search.data
        assert new_search.data[0].id     

    def test_03_customer_pagination_before(self):
        self.client.api_key = '1tv5yJp3xnVZ7eK67m4h'
        customer1 = self.client.Customer.create(self.customer_object.copy())
        customer2 = self.client.Customer.create(self.customer_object.copy())
        customer3 = self.client.Customer.create(self.customer_object.copy())
        query = {}
        query["previous"] = customer1.id
        customers = self.client.Customer.where(query)
        new_search = customers.next()
        
        custs = new_search.data
        assert custs[0].id

    def test_04_order_all(self):
        self.client.api_key = '1tv5yJp3xnVZ7eK67m4h'
        self.client.Order.create(self.order_object.copy())
        self.client.Order.create(self.order_object.copy())
        self.client.Order.create(self.order_object.copy())
        
        orders = self.client.Order.where()
        assert orders[0].id

    def test_05_order_pagination_next(self):
        self.client.api_key = '1tv5yJp3xnVZ7eK67m4h'
        order1 = self.client.Order.create(self.order_object.copy())
        order2 = self.client.Order.create(self.order_object.copy())
        order3 = self.client.Order.create(self.order_object.copy())
        query = {}
        query["next"] = order1.id
        orders = self.client.Order.where(query)
        new_search = orders.next()

        orders = new_search.data
        assert new_search.data[0].id     

    def test_05_order_pagination_before(self):
        self.client.api_key = '1tv5yJp3xnVZ7eK67m4h'
        order1 = self.client.Order.create(self.order_object.copy())
        order2 = self.client.Order.create(self.order_object.copy())
        order3 = self.client.Order.create(self.order_object.copy())
        query = {}
        query["previous"] = order1.id
        orders = self.client.Order.where(query)
        new_search = orders.next()

        orders = new_search.data
        assert new_search.data[0].id    

        