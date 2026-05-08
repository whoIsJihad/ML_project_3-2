# Map of Content 

This directory contains notes on the structure of the internet and routing protocols.

## [[Autonomous Systems]]
This note describes Autonomous Systems (ASs), their structure, and the different types of routers within an AS. It covers the distinction between Stub AS and Non-stub AS, and the roles of area-border routers, border routers, and the backbone area.

## [[BGP and Interdomain Routing]] 
This note focuses on the Border Gateway Protocol (BGP), the protocol used for inter-domain routing between different Autonomous Systems. It explains that BGP is a path vector protocol and its goal is to find a valid path, not necessarily the most optimal one, based on policy and business considerations.

## [[Internet Structure and ISP Hierarchy]]
This note illustrates the hierarchical structure of the Internet, composed of different tiers of Internet Service Providers (ISPs), from large Tier-1 ISPs that form the global backbone to smaller ISPs and access networks.

## [[ISP Business Relationships]]
This note explains the business relationships between ISPs, focusing on the concepts of "transit" and "peering". It describes the customer-provider hierarchy and the economic and policy-driven decisions behind peering agreements.

## [[Routing Protocols]]
This note provides an overview of the two main types of routing protocols:
- **Intra-domain routing protocols (IGPs):** like OSPF, used for routing within a single Autonomous System.
- **Inter-domain routing protocols (EGPs):** like BGP, used for routing between different Autonomous Systems.

## [[Type of Service and DiffServ]]
This note covers the "Type of Service" (ToS) field in the IP header, which is used to differentiate traffic based on characteristics like delay, throughput, and reliability. It also introduces Differentiated Services (DiffServ) as a mechanism for providing Quality of Service (QoS) based on the ToS field.
