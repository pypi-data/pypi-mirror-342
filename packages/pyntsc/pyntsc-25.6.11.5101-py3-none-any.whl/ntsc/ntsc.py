import os
import time
import json
import pprint
import requests
import ipaddress
import socket
import platform
import subprocess


class ToolsUtils:
    @staticmethod
    def to_dict(instance):
        """
        * 工具类封装
        :param :
        :return:
        """
        return {
            k: (v[0] if isinstance(v, tuple) else v)
            for k, v in instance.__dict__.items()
            if not k.startswith("_")
        }


class NetworkUtils:
    @staticmethod
    def ping_host(host, count=1, timeout=1):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        try:
            result = subprocess.run(
                ['ping', param, str(count), host],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return result.returncode == 0
        except Exception:
            return False
    
    @staticmethod
    def check_port(host, port, timeout=1):
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except Exception:
            return False


class PortSpeedLimit:
    def __init__(self):
        self.LimitMode = "Interface"
        self.LimitType = "case"
        self.LimitGraph = "fixed"
        self.SpeedLimit = 0
        self.Accumulate = "slice_add"
        self.FlushTokenUsecond = "1000"
        self.Name = "HttpCps"
        self.TestType = "HttpCps"
    
    def to_dict(self):
        return self.__dict__


class SimUserSpeedLimit:
    def __init__(self):
        self.LimitMode = "Interface"
        self.LimitType = "simuser"
        self.LimitGraph = "fixed"
        self.Accumulate = "slice_add"
        self.FlushTokenUsecond = "1000"
        self.IterationStandard = 95
        self.IterationRange = 5
        self.StabilizeTestTime = 5
        self.Name = "HttpCps"
        self.TestType = "HttpCps"
    
    def to_dict(self):
        return self.__dict__


class PacketCapture:
    def __init__(self):
        self.CapturePacketEnable = "no"
        self.MgmtIp = "192.168.15.100"
        self.PhysicalPort = "port1"
        self.CaptureProtocol = "None"
        self.CaptureMessage = "All"
    
    def set_capture_packet_enable(self, enable: str):
        if enable in ["yes", "no"]:
            self.CapturePacketEnable = enable
        else:
            raise ValueError(f"The input param {enable} is an invalid identifier.")
    
    def set_mgmt_ip(self, ip: str):
        try:
            # 尝试将字符串转换为 IPv4 地址对象
            ipv4_obj = ipaddress.IPv4Address(ip)
            # print(ipv4_obj)
            self.MgmtIp = ipv4_obj
        except ValueError:
            # 若转换失败，抛出异常提示字符串不是有效的 IPv4 地址
            raise ValueError(f"The input param {ip} is an invalid identifier.。")
    
    def set_physical_port(self, port: str):
        if port in ["port1", "port2", "port3", "port4"]:
            self.PhysicalPort = port
        else:
            raise ValueError(f"The input param '{port}' is an invalid identifier.")
    
    def set_capture_protocol(self, protocol: str):
        if protocol in ["ALL", "None", "ARP", "DNP", "ICMP", "IGMP", "TCP", "UDP"]:
            self.PhysicalPort = protocol
        else:
            raise ValueError(f"The input param '{protocol}' is an invalid identifier.")
    
    def set_capture_message(self, message: str):
        if message in ["ALL", "None", "PAUSE", "TCP_SYN", "TCP_RE"]:
            self.CaptureMessage = message
        else:
            raise ValueError(f"The input param '{message}' is an invalid identifier.")
    
    def set_capture_ip(self, ip_str: str):
        try:
            # 尝试将字符串转换为 IPv4 地址
            ip = ipaddress.IPv4Address(ip_str)
            return ip
        except ValueError:
            try:
                # 若不是 IPv4 地址，尝试转换为 IPv6 地址
                ip = ipaddress.IPv6Address(ip_str)
                return ip
            except ValueError:
                # 若既不是 IPv4 也不是 IPv6 地址，抛出异常
                raise ValueError(f"The input param '{ip_str}' is an invalid identifier.")
    
    def set_capture_port(self, port: str):
        if 0 <= int(port) <= 65535:
            self.CapturePort = port
        else:
            raise ValueError(f"The input param '{port}' is an invalid identifier.")
    
    def set_capture_max_file_size(self, max_file_size: str):
        if 0 <= int(max_file_size) <= 2000:
            self.CaptureMaxFileSize = max_file_size
        else:
            raise ValueError(f"The input param {max_file_size} is an invalid identifier.")
    
    def set_capture_packat_count(self, packat_count: str):
        if 0 <= int(packat_count) <= 12000000:
            self.CapturePackatCount = packat_count
        else:
            raise ValueError(f"The input param {packat_count} is an invalid identifier.")
    
    def to_dict(self):
        return self.__dict__


class PacketFilter:
    def __init__(self):
        self.PacketFilterEnable = "no"
        self.FilterAction = "Drop"
        self.FilteringProtocol = "All"
        self.FilteringIPVersion = "v4"
        self.SrcPortMathes = "Eq"
        self.DstPortMathes = "Eq"
    
    def set_capture_packet_enable(self, enable: str):
        if enable in ["yes", "no"]:
            self.CapturePacketEnable = enable
        else:
            raise ValueError(f"The input param '{enable}' is an invalid identifier.")
    
    def set_filter_action(self, action: str):
        if action in ["Drop", "Queue"]:
            self.PhysicalPort = action
        else:
            raise ValueError(f"The input param '{action}' is an invalid identifier.。")
    
    def set_filtering_protocol(self, protocol: str):
        if protocol in ["All", "TCP", "UDP"]:
            self.PhysicalPort = protocol
        else:
            raise ValueError(f"The input param '{protocol}' is an invalid identifier.")
    
    def set_filtering_ip_Version(self, Version: str):
        if Version in ["v4", "v6"]:
            self.PhysicalPort = Version
        else:
            raise ValueError(f"The input param '{Version}' is an invalid identifier.")
    
    def set_src_port_mathes(self, src_port_mathes: str):
        if src_port_mathes in ["Eq", "Neq"]:
            self.PhysicalPort = src_port_mathes
        else:
            raise ValueError(f"The input param '{src_port_mathes}' is an invalid identifier.")
    
    def set_dst_port_mathes(self, dst_port_mathes: str):
        if dst_port_mathes in ["Eq", "Neq"]:
            self.PhysicalPort = dst_port_mathes
        else:
            raise ValueError(f"The input param '{dst_port_mathes}' is an invalid identifier.")
    
    def set_filtering_src_ipv4(self, ip: str):
        try:
            ipv4_obj = ipaddress.IPv4Address(ip)
            self.FilteringSrcIpv4 = ipv4_obj
        except ValueError:
            raise ValueError(f"The input param {ip} is an invalid identifier.")
    
    def set_filtering_src_ipv6(self, ip: str):
        try:
            ipv6_obj = ipaddress.IPv6Address(ip)
            self.FilteringSrcIpv6 = ipv6_obj
        except ValueError:
            raise ValueError(f"The input param {ip} is an invalid identifier.")
    
    def set_filtering_dst_ipv4(self, ip: str):
        try:
            ipv4_obj = ipaddress.IPv4Address(ip)
            self.FilteringDstIpv4 = ipv4_obj
        except ValueError:
            raise ValueError(f"The input param {ip} is an invalid identifier.")
    
    def set_filtering_dst_ipv6(self, ip: str):
        try:
            ipv6_obj = ipaddress.IPv6Address(ip)
            self.FilteringDstIpv6 = ipv6_obj
        except ValueError:
            raise ValueError(f"The input param {ip} is an invalid identifier.")
    
    def set_filtering_src_port(self, src_port: str):
        if 0 <= int(src_port) <= 65535:
            self.FilteringSrcPort = src_port
        else:
            raise ValueError(f"The input param '{src_port}' is an invalid identifier.")
    
    def set_filtering_dst_port(self, dst_port: str):
        if 0 <= int(dst_port) <= 65535:
            self.FilteringDstPort = dst_port
        else:
            raise ValueError(f"The input param '{dst_port}' is an invalid identifier.")
    
    def to_dict(self):
        return self.__dict__


class NetworkControlConfig:
    """通用参数配置类"""
    
    def __init__(self):
        # 时间控制参数
        self.WaitPortsUpSecond = 30
        self.StartClientDelaySecond = 2
        self.ArpNsnaTimeoutSeconds = 30
        self.MessageSyncTimeoutSecond = 30
        self.MaxPortDownTime = 10
        self.NetworkCardUpTime = 5
        
        # 协议控制参数
        self.TimerSchedOutAction = "Warning"
        self.TCLRunMoment = "start"
        self.SendGratuitousArp = "yes"
        self.BcastNextMacOnlyFirstIP = "no"
        self.PingConnectivityCheck = "yes"
        self.PingTimeOutSecond = 15
        
        # 网络配置参数
        self.NetWork = "默认协议栈选项"
        self.IPChangeAlgorithm = "Increment"
        self.IPAddLoopPriority = "Client"
        self.PortChangeAlgorithm = "Increment"
        self.Layer4PortAddStep = 1
        
        # 高级配置
        self.IpPortMapping = "no"
        self.IpPortMappingTxt = ""
        self.Piggybacking = "yes"
        self.FlowRatio = "1:1"
        self.MaxEventPerLoop = 64
        self.TcpTimerSchedUsecond = 100
        self.MaxTimerPerLoop = 16
        self.TwotierByteStatistics = "no"
        self.Layer4PacketsCount = "no"
        self.SystemTimerDebug = "no"
        self.NicPhyRewrite = "yes"
        self.StopCloseAgeingSecond = 2
        self.TcpStopCloseMethod = "Reset"
        self.TcpPerfectClose = "no"
        self.PromiscuousMode = "no"
        self.TesterMessagePort = 2002
    
    def set_wait_ports_up_second(self, seconds: int):
        self.WaitPortsUpSecond = seconds
    
    def set_start_client_delay(self, seconds: int):
        self.StartClientDelaySecond = seconds
    
    def set_arp_nsna_timeout(self, seconds: int):
        self.ArpNsnaTimeoutSeconds = seconds
    
    def set_message_sync_timeout(self, seconds: int):
        self.MessageSyncTimeoutSecond = seconds
    
    def set_max_port_down_time(self, seconds: int):
        self.MaxPortDownTime = seconds
    
    def set_network_card_up_time(self, seconds: int):
        self.NetworkCardUpTime = seconds
    
    def set_timer_sched_action(self, action: str):
        self.TimerSchedOutAction = action
    
    def set_tcl_run_moment(self, moment: str):
        self.TCLRunMoment = moment
    
    def set_send_gratuitous_arp(self, enable: bool):
        self.SendGratuitousArp = "yes" if enable else "no"
    
    def set_bcast_mac_policy(self, enable: bool):
        self.BcastNextMacOnlyFirstIP = "yes" if enable else "no"
    
    def set_ping_check(self, enable: bool):
        self.PingConnectivityCheck = "yes" if enable else "no"
    
    def set_ping_timeout(self, seconds: int):
        self.PingTimeOutSecond = seconds
    
    def set_network_stack(self, stack_name: str):
        self.NetWork = stack_name
    
    def set_ip_change_algo(self, algorithm: str):
        self.IPChangeAlgorithm = algorithm
    
    def set_ip_loop_priority(self, priority: str):
        self.IPAddLoopPriority = priority
    
    def set_port_change_algo(self, algorithm: str):
        self.PortChangeAlgorithm = algorithm
    
    def set_layer4_port_add_step(self, step: int):
        self.Layer4PortAddStep = step
    
    def set_ip_port_mapping(self, enable: bool):
        self.IpPortMapping = "yes" if enable else "no"
    
    def set_piggybacking(self, enable: bool):
        self.Piggybacking = "yes" if enable else "no"
    
    def set_flow_ratio(self, ratio: str):
        self.FlowRatio = ratio
    
    def set_max_event_per_loop(self, count: int):
        self.MaxEventPerLoop = count
    
    def set_tcp_timer_sched(self, microseconds: int):
        self.TcpTimerSchedUsecond = microseconds
    
    def set_max_timer_per_loop(self, count: int):
        self.MaxTimerPerLoop = count
    
    def set_twotier_byte_stats(self, enable: bool):
        self.TwotierByteStatistics = "yes" if enable else "no"
    
    def set_layer4_packets_count(self, enable: bool):
        self.Layer4PacketsCount = "yes" if enable else "no"
    
    def set_system_timer_debug(self, enable: bool):
        self.SystemTimerDebug = "yes" if enable else "no"
    
    def set_nic_phy_rewrite(self, enable: bool):
        self.NicPhyRewrite = "yes" if enable else "no"
    
    def set_stop_close_ageing(self, seconds: int):
        self.StopCloseAgeingSecond = seconds
    
    def set_tcp_stop_close_method(self, method: str):
        self.TcpStopCloseMethod = method
    
    def set_tcp_perfect_close(self, enable: bool):
        self.TcpPerfectClose = "yes" if enable else "no"
    
    def set_promiscuous_mode(self, enable: bool):
        self.PromiscuousMode = "yes" if enable else "no"
    
    def set_tester_message_port(self, port: int):
        self.TesterMessagePort = port
    
    # 生成字典格式
    def to_dict(self):
        return ToolsUtils.to_dict(self)


class ClientSubnet:
    
    def __init__(self):
        # 启用（默认：yes）
        self.SubnetEnable = 'yes'
        # 子网编号（默认：1）
        self.SubnetNumber = '1'
        # IP地址版本（默认v4）
        self.SubnetVersion = "v4"
        # IP地址范围（默认：17.1.2.2+100）
        self.IpAddrRange = '17.1.2.2+100'
        # 步进值（默认：0.0.0.1）
        self.SubnetStep = '0.0.0.1'
        # 掩码（默认：16）
        self.Netmask = '16'
        # 网关地址（默认：#disabled）
        self.Gateway = '#disabled'
        # 服务端类型（默认：IP）
        self.ServerAddressFormat = 'IP'
        # 服务器IP地址或域名（默认：17.1.2.2+100）
        self.ServerIPRange = '17.1.2.2+100'
        # 当服务端类型选择Port时，指定服务端端口，指定服务端子网编号
        self.SubnetServicePort = 'port2'
        self.PeerServerSubnet = '1'
        # VLAN ID（默认：1#disabled）
        self.VlanID = '1#disabled'
        self.SubnetRole = 'client'
    
    def init_by_dict(self, **kwargs):
        # 用字典创建对象
        self.__dict__.update(kwargs)
    
    def set_subnet_enable(self, enable):
        if enable not in ['yes', 'no']:
            raise ValueError("The set value is not valid. The valid value is 'yes' or 'no'")
        self.SubnetEnable = enable
    
    def set_subnet_number(self, subnet_number):
        if not subnet_number:
            raise ValueError("The subnet number cannot be empty")
        self.SubnetNumber = subnet_number
    
    def set_subnet_version(self, subnet_version):
        if subnet_version not in ['v4', 'v6']:
            raise ValueError("The set value is not valid. The valid value is 'v4' or 'v6'")
        self.SubnetVersion = subnet_version
    
    def set_ip_addr_range(self, ip_addr_range):
        if not ip_addr_range:
            raise ValueError("IP address range cannot be empty")
        
        for ip_addr in ip_addr_range.split(","):
            if ip_addr.find("+") != -1:
                ipaddress.ip_address(ip_addr.split("+")[0])
            elif ip_addr.find("-") != -1:
                for ip_split in ip_addr.split("-"):
                    ipaddress.ip_address(ip_split)
        self.IpAddrRange = ip_addr_range
    
    def set_subnet_step(self, subnet_step):
        if not subnet_step:
            raise ValueError("The step value cannot be empty")
        ipaddress.ip_address(subnet_step)
        self.SubnetStep = subnet_step
    
    def set_netmask(self, netmask):
        if not netmask:
            raise ValueError("The mask cannot be empty")
        self.Netmask = netmask
    
    def set_gateway(self, gateway):
        if not gateway:
            self.Gateway = "#disabled"
        else:
            ipaddress.ip_address(gateway)
            self.Gateway = gateway
    
    def set_server_address_format(self, server_address_format):
        if server_address_format not in ['IP', 'Port']:
            raise ValueError("The set value is not valid. The valid value is 'IP' or 'Port'")
        self.ServerAddressFormat = server_address_format
    
    def set_server_ip_range(self, server_ip_range):
        if not server_ip_range:
            raise ValueError("The server ip address or domain name cannot be empty")
        for ip_addr in server_ip_range.split(","):
            if ip_addr.find("+") != -1:
                ipaddress.ip_address(ip_addr.split("+")[0])
            elif ip_addr.find("-") != -1:
                for ip_split in ip_addr.split("-"):
                    ipaddress.ip_address(ip_split)
        self.ServerIPRange = server_ip_range
    
    def set_subnet_service_port(self, server_port):
        """
        * setting the server port
        :param server_port:
        :return:
        """
        if not server_port:
            raise ValueError("The server port cannot be empty")
        self.SubnetServicePort = server_port
    
    def set_peer_server_subnet(self, server_subnet):
        """
        * set the subnet number of the server
        :param server_subnet:
        :return:
        """
        if not server_subnet:
            raise ValueError("The subnet number of the server cannot be empty")
        self.PeerServerSubnet = server_subnet
    
    def set_vlan_id(self, vlan_id):
        if not vlan_id:
            self.VlanID = "1#disabled"
        else:
            self.VlanID = vlan_id
    
    def to_dict(self):
        if self.ServerAddressFormat == "IP":
            try:
                del self.SubnetServicePort
                del self.PeerServerSubnet
            except AttributeError:
                pass
        else:
            try:
                del self.ServerIPRange
            except AttributeError:
                pass
        return self.__dict__


class ServerSubnet:
    def __init__(self):
        # 启用（默认：yes）
        self.SubnetEnable = 'yes'
        # 子网编号（默认1）
        self.SubnetNumber = '1'
        # IP地址版本
        self.SubnetVersion = "v4"
        # IP地址范围（默认：17.1.1.2+10）
        self.IpAddrRange = '17.1.1.2+10'
        # 步进值（默认：0.0.0.1）
        self.SubnetStep = '0.0.0.1'
        # 掩码（默认：16）
        self.Netmask = '16'
        # 网关地址（默认：#disabled）
        self.Gateway = '#disabled'
        # VLAN ID（默认：1#disabled）
        self.VlanID = '1#disabled'
        # 角色
        self.SubnetRole = 'server'
    
    def init_by_dict(self, **kwargs):
        # 用字典创建
        self.__dict__.update(kwargs)
    
    def set_subnet_enable(self, enable):
        if enable not in ['yes', 'no']:
            raise ValueError("The set value is not valid. The valid value is 'yes' or 'no'")
        self.SubnetEnable = enable
    
    def set_subnet_number(self, subnet_number):
        if not subnet_number:
            raise ValueError("The subnet number cannot be empty")
        self.SubnetNumber = subnet_number
    
    def set_subnet_version(self, subnet_version):
        if subnet_version not in ['v4', 'v6']:
            raise ValueError("The set value is not valid. The valid value is 'v4' or 'v6'")
        self.SubnetVersion = subnet_version
    
    def set_ip_addr_range(self, ip_addr_range):
        if not ip_addr_range:
            raise ValueError("IP address range cannot be empty")
        
        for ip_addr in ip_addr_range.split(","):
            if ip_addr.find("+") != -1:
                ipaddress.ip_address(ip_addr.split("+")[0])
            elif ip_addr.find("-") != -1:
                for ip_split in ip_addr.split("-"):
                    ipaddress.ip_address(ip_split)
        self.IpAddrRange = ip_addr_range
    
    def set_subnet_step(self, subnet_step):
        if not subnet_step:
            raise ValueError("The step value cannot be empty")
        ipaddress.ip_address(subnet_step)
        self.SubnetStep = subnet_step
    
    def set_netmask(self, netmask):
        if not netmask:
            raise ValueError("The mask cannot be empty")
        self.Netmask = netmask
    
    def set_gateway(self, gateway):
        if not gateway:
            self.Gateway = "#disabled"
        else:
            ipaddress.ip_address(gateway)
            self.Gateway = gateway
    
    def set_vlan_id(self, vlan_id):
        if not vlan_id:
            self.VlanID = "1#disabled"
        else:
            self.VlanID = vlan_id
    
    def to_dict(self):
        return self.__dict__


# 反向代理
class ReverseProxyClient:
    def __init__(self):
        # 启用（默认：yes）
        self.SubnetEnable = 'yes'
        # 子网编号（默认：1）
        self.SubnetNumber = '1'
        # IP地址版本（默认v4）
        self.SubnetVersion = "v4"
        # IP地址范围（默认：17.1.2.2+100）
        self.IpAddrRange = '17.1.2.2+100'
        # 步进值（默认：0.0.0.1）
        self.SubnetStep = '0.0.0.1'
        # 掩码（默认：16）
        self.Netmask = '16'
        # 网关地址（默认：#disabled）
        self.Gateway = '#disabled'
        # 代理服务IP地址
        self.ProxyIpAddrRange = ''
        # VLAN ID（默认：1#disabled）
        self.VlanID = '1#disabled'
        self.SubnetRole = 'client'
    
    def init_by_dict(self, **kwargs):
        # 用字典创建
        self.__dict__.update(kwargs)
    
    def set_subnet_enable(self, enable):
        if enable not in ['yes', 'no']:
            raise ValueError("The set value is not valid. The valid value is 'yes' or 'no'")
        self.SubnetEnable = enable
    
    def set_subnet_number(self, subnet_number):
        if not subnet_number:
            raise ValueError("The subnet number cannot be empty")
        self.SubnetNumber = subnet_number
    
    def set_subnet_version(self, subnet_version):
        if subnet_version not in ['v4', 'v6']:
            raise ValueError("The set value is not valid. The valid value is 'v4' or 'v6'")
        self.SubnetVersion = subnet_version
    
    def set_ip_addr_range(self, ip_addr_range):
        if not ip_addr_range:
            raise ValueError("IP address range cannot be empty")
        
        for ip_addr in ip_addr_range.split(","):
            if ip_addr.find("+") != -1:
                ipaddress.ip_address(ip_addr.split("+")[0])
            elif ip_addr.find("-") != -1:
                for ip_split in ip_addr.split("-"):
                    ipaddress.ip_address(ip_split)
        self.IpAddrRange = ip_addr_range
    
    def set_subnet_step(self, subnet_step):
        if not subnet_step:
            raise ValueError("The step value cannot be empty")
        ipaddress.ip_address(subnet_step)
        self.SubnetStep = subnet_step
    
    def set_netmask(self, netmask):
        if not netmask:
            raise ValueError("The mask cannot be empty")
        self.Netmask = netmask
    
    def set_gateway(self, gateway):
        if not gateway:
            self.Gateway = "#disabled"
        else:
            ipaddress.ip_address(gateway)
            self.Gateway = gateway
    
    def set_proxy_ip_addr_range(self, proxy_ip_addr_range):
        if not proxy_ip_addr_range:
            raise ValueError("The proxy server ip address cannot be empty")
        self.ProxyIpAddrRange = proxy_ip_addr_range
    
    def set_vlan_id(self, vlan_id):
        if not vlan_id:
            self.VlanID = "1#disabled"
        else:
            self.VlanID = vlan_id
    
    def to_dict(self):
        if not self.ProxyIpAddrRange:
            raise ValueError("The proxy server ip address cannot be empty")
        return self.__dict__


# 正向代理
class ForwardProxyClient:
    def __init__(self):
        # 启用（默认：yes）
        self.SubnetEnable = 'yes'
        # 子网编号（默认：1）
        self.SubnetNumber = '1'
        # IP地址版本（默认v4）
        self.SubnetVersion = "v4"
        # IP地址范围（默认：17.1.2.2+100）
        self.IpAddrRange = '17.1.2.2+100'
        # 步进值（默认：0.0.0.1）
        self.SubnetStep = '0.0.0.1'
        # 掩码（默认：16）
        self.Netmask = '16'
        # 网关地址（默认：#disabled）
        self.Gateway = '#disabled'
        # 代理服务IP地址
        self.ProxyIpAddrRange = ''
        # 服务端类型（默认：IP）
        self.ServerAddressFormat = 'IP'
        # 服务器IP地址或域名（默认：17.1.2.2+100）
        self.ServerIPRange = '17.1.2.2+100'
        # 当服务端类型选择Port时，指定服务端端口，指定服务端子网编号
        self.SubnetServicePort = 'port2'
        self.PeerServerSubnet = '1'
        # VLAN ID（默认：1#disabled）
        self.VlanID = '1#disabled'
        self.SubnetRole = 'client'
    
    def init_by_dict(self, **kwargs):
        # 用字典创建
        self.__dict__.update(kwargs)
    
    def set_subnet_enable(self, enable):
        if enable not in ['yes', 'no']:
            raise ValueError("The set value is not valid. The valid value is 'yes' or 'no'")
        self.SubnetEnable = enable
    
    def set_subnet_number(self, subnet_number):
        if not subnet_number:
            raise ValueError("The subnet number cannot be empty")
        self.SubnetNumber = subnet_number
    
    def set_subnet_version(self, subnet_version):
        if subnet_version not in ['v4', 'v6']:
            raise ValueError("The set value is not valid. The valid value is 'v4' or 'v6'")
        self.SubnetVersion = subnet_version
    
    def set_ip_addr_range(self, ip_addr_range):
        if not ip_addr_range:
            raise ValueError("IP address range cannot be empty")
        
        for ip_addr in ip_addr_range.split(","):
            if ip_addr.find("+") != -1:
                ipaddress.ip_address(ip_addr.split("+")[0])
            elif ip_addr.find("-") != -1:
                for ip_split in ip_addr.split("-"):
                    ipaddress.ip_address(ip_split)
        self.IpAddrRange = ip_addr_range
    
    def set_subnet_step(self, subnet_step):
        if not subnet_step:
            raise ValueError("The step value cannot be empty")
        ipaddress.ip_address(subnet_step)
        self.SubnetStep = subnet_step
    
    def set_netmask(self, netmask):
        if not netmask:
            raise ValueError("The mask cannot be empty")
        self.Netmask = netmask
    
    def set_gateway(self, gateway):
        if not gateway:
            self.Gateway = "#disabled"
        else:
            ipaddress.ip_address(gateway)
            self.Gateway = gateway
    
    def set_proxy_ip_addr_range(self, proxy_ip_addr_range):
        if not proxy_ip_addr_range:
            raise ValueError("The proxy server ip address cannot be empty")
        self.ProxyIpAddrRange = proxy_ip_addr_range
    
    def set_server_address_format(self, server_address_format):
        if server_address_format not in ['IP', 'Port']:
            raise ValueError("The set value is not valid. The valid value is 'IP' or 'Port'")
        self.ServerAddressFormat = server_address_format
    
    def set_server_ip_range(self, server_ip_range):
        if not server_ip_range:
            raise ValueError("The server ip address or domain name cannot be empty")
        for ip_addr in server_ip_range.split(","):
            if ip_addr.find("+") != -1:
                ipaddress.ip_address(ip_addr.split("+")[0])
            elif ip_addr.find("-") != -1:
                for ip_split in ip_addr.split("-"):
                    ipaddress.ip_address(ip_split)
        self.ServerIPRange = server_ip_range
    
    def set_subnet_service_port(self, server_port):
        """
        * setting the server port
        :param server_port:
        :return:
        """
        if not server_port:
            raise ValueError("The server port cannot be empty")
        self.SubnetServicePort = server_port
    
    def set_peer_server_subnet(self, server_subnet):
        """
        * set the subnet number of the server
        :param server_subnet:
        :return:
        """
        if not server_subnet:
            raise ValueError("The subnet number of the server cannot be empty")
        self.PeerServerSubnet = server_subnet
    
    def set_vlan_id(self, vlan_id):
        if not vlan_id:
            self.VlanID = "1#disabled"
        else:
            self.VlanID = vlan_id
    
    def to_dict(self):
        if self.ServerAddressFormat == "IP":
            try:
                del self.SubnetServicePort
                del self.PeerServerSubnet
            except AttributeError:
                pass
        else:
            try:
                del self.ServerIPRange
            except AttributeError:
                pass
        return self.__dict__


class BaseSubnet:
    @classmethod
    def create_subnet(cls, dut_role, proxy_mode=''):
        if dut_role == "Gateway":
            client_subnet = ClientSubnet()
            server_subnet = ServerSubnet()
            # print(client_subnet.to_dict())
            # print(server_subnet.to_dict())
            return client_subnet, server_subnet
        elif dut_role == "Client":
            client_subnet = ClientSubnet()
            # print(client_subnet.to_dict())
            return client_subnet
        elif dut_role == "Server":
            server_subnet = ServerSubnet()
            # print(server_subnet.to_dict())
            return server_subnet
        elif dut_role == "Proxy":
            if not proxy_mode:
                raise ValueError("If the device under test is a proxy device, parameter 'proxy_mode' must be specified")
            if proxy_mode not in ["Reverse", "Forward"]:
                raise ValueError("The set value is not valid. The valid value is 'Reverse' or 'Forward'")
            if proxy_mode == "Reverse":
                reverse_proxy_client_subnet = ReverseProxyClient()
                reverse_proxy_client_subnet.set_proxy_ip_addr_range("17.1.1.1")
                # print(reverse_proxy_client_subnet.to_dict())
                server_subnet = ServerSubnet()
                # print(server_subnet.to_dict())
                return reverse_proxy_client_subnet, server_subnet
            else:
                forward_proxy_client_subnet = ForwardProxyClient()
                forward_proxy_client_subnet.set_proxy_ip_addr_range("18.1.1.1")
                # print(forward_proxy_client_subnet.to_dict())
                server_subnet = ServerSubnet()
                # print(server_subnet.to_dict())
                return forward_proxy_client_subnet, server_subnet


BaseSubnet.create_subnet("Proxy", "Reverse")


# 定义头部校验和配置类，用于管理 IPV4、TCP 和 UDP 的头部校验和类型
class HeadChecksumConf:
    def __init__(self, IPV4HeadChecksumType="auto", TCPHeadChecksumType="auto", UDPHeadChecksumType="auto"):
        """
        初始化头部校验和配置类。

        Args:
            IPV4HeadChecksumType (str, optional): IPV4 头部校验和类型，默认为 "auto"。
            TCPHeadChecksumType (str, optional): TCP 头部校验和类型，默认为 "auto"。
            UDPHeadChecksumType (str, optional): UDP 头部校验和类型，默认为 "auto"。
        """
        self.IPV4HeadChecksumType = IPV4HeadChecksumType
        self.TCPHeadChecksumType = TCPHeadChecksumType
        self.UDPHeadChecksumType = UDPHeadChecksumType
    
    def to_dict(self):
        """
        将头部校验和配置转换为字典。

        Returns:
            dict: 包含 IPV4、TCP 和 UDP 头部校验和类型的字典。
        """
        return {
            "IPV4HeadChecksumType": self.IPV4HeadChecksumType,
            "TCPHeadChecksumType": self.TCPHeadChecksumType,
            "UDPHeadChecksumType": self.UDPHeadChecksumType
        }


# 定义网络接口卡 (NIC) 配置类，用于管理 NIC 的各项配置
class NICConfiguration:
    def __init__(self):
        """
        初始化网络接口卡配置类，设置各项默认配置。
        """
        self.MacMasquerade = "A2:01#disabled"
        self.PortSpeedDetectMode = "Autoneg"
        self.PortRXRSS = "no"
        self.nictype = "PERF"
        self.receivequeue = "4"
        self.nb_txd = 4096
        self.nb_rxd = 4096
        self.NextPortMacMethod = "ARP_NSNA#disabled"
        self.sendqueue = "4"
        self.device = "NetiTest IT2X010GF47LA 1G/10G SmartNIC"
        self.TesterPortMacAddress = "68:91:d0:66:b1:b6#disabled"
        # 初始化头部校验和配置
        self.HeadChecksumConf = HeadChecksumConf()
    
    def to_dict(self):
        """
        将网络接口卡配置转换为字典。

        Returns:
            dict: 包含 NIC 所有配置信息的字典。
        """
        return {
            "MacMasquerade": self.MacMasquerade,
            "PortSpeedDetectMode": self.PortSpeedDetectMode,
            "PortRXRSS": self.PortRXRSS,
            "nictype": self.nictype,
            "receivequeue": self.receivequeue,
            "nb_txd": self.nb_txd,
            "nb_rxd": self.nb_rxd,
            "NextPortMacMethod": self.NextPortMacMethod,
            "sendqueue": self.sendqueue,
            # 将实例的 device 属性添加到字典中
            "device": self.device,
            # 将实例的 TesterPortMacAddress 属性添加到字典中
            "TesterPortMacAddress": self.TesterPortMacAddress,
            # 将 HeadChecksumConf 实例转换为字典并添加到结果字典中
            "HeadChecksumConf": self.HeadChecksumConf.to_dict()
        }
    
    def to_json(self, indent=4):
        """
        将 NICConfiguration 实例转换为 JSON 格式的字符串。

        Args:
            indent (int, optional): JSON 字符串的缩进空格数，默认为 4。

        Returns:
            str: 包含 NICConfiguration 配置信息的 JSON 格式字符串。
        """
        return json.dumps(self.to_dict(), indent=indent)


class GTPUTunnel:
    """
    表示 GTPU封装 隧道的配置类，用于管理 GTPU 隧道的各项参数。
    """
    
    def __init__(self):
        """
        初始化 GPTUTunnel 类的实例，设置默认的 GTPU 隧道参数。
        """
        self.GTPUEnable = "no"  # 指示 GTPU 隧道是否启用
        self.TunnelIPVersion = 4  # 隧道使用的 IP 版本，默认为 IPv4
        self.TunnelPort1 = 2152  # 本端GTPU隧道端口
        self.TunnelTeid1 = 1  # 对端GTPU隧道起始ID
        self.TunnelQfi = 1  # GTPU扩展头数值
        self.TunnelIPAddr1 = "172.1.1.2"  # 本端GTPU IP地址
        self.TunnelIPAddr2 = "172.1.2.2"  # 对端GTPU IP地址
        self.GtpuNetworkMask = 16  # GTPU 网络掩码
    
    def set_gtpu_enable(self, enable: bool):
        """
        设置 GTPU 隧道的启用状态。

        Args:
            enable (bool): 若为 True，则启用 GTPU 隧道；若为 False，则禁用。
        """
        self.GTPUEnable = "yes" if enable else "no"
    
    def set_tunnel_ip_version(self, version: int):
        """
        设置 GTPU 隧道使用的 IP 版本。

        Args:
            version (int): 要设置的 IP 版本，必须为 4 或 6。

        Raises:
            ValueError: 当传入的 IP 版本不是 4 或 6 时抛出。
        """
        if version in (4, 6):
            self.TunnelIPVersion = version
        else:
            raise ValueError("Only IP version 4 or 6 is supported.")
    
    def set_tunnel_port(self, port: int):
        """
        设置 GTPU 隧道的端口号。

        Args:
            port (int): 要设置的端口号。
        """
        self.TunnelPort1 = port
    
    def set_tunnel_teid(self, teid: int):
        """
        设置 对端GTPU隧道起始ID。

        Args:
            teid (int): 要设置的 TEID。
        """
        self.TunnelTeid1 = teid
    
    def set_tunnel_qfi(self, qfi: int):
        """
        设置 GTPU扩展头数值。

        Args:
            qfi (int): 要设置的 QFI。
        """
        self.TunnelQfi = qfi
    
    def set_tunnel_ip_local(self, ip1: str):
        """
        设置 GTPU 本端 IP 地址。

        Args:
            ip1 (str): 第一个 IP 地址。
            ip2 (str): 第二个 IP 地址。
        """
        self.TunnelIPAddr1 = ip1
    
    def set_tunnel_ip_local(self, ip2: str):
        """
        设置 GTPU 对端 IP 地址。

        Args:
            ip2 (str): 第一个 IP 地址。
        """
        self.TunnelIPAddr1 = ip2
    
    def set_network_mask(self, mask: int):
        """
        设置 GTPU 网络掩码。

        Args:
            mask (int): 要设置的网络掩码，必须在 0 到 32 之间。

        Raises:
            ValueError: 当传入的网络掩码不在 0 到 32 之间时抛出。
        """
        if 0 <= mask <= 32:
            self.GtpuNetworkMask = mask
        else:
            raise ValueError("Invalid network mask, must be between 0 and 32.")
    
    def to_dict(self):
        """
        将 GPTUTunnel 实例的属性转换为字典。

        Returns:
            dict: 包含 GTPU 隧道配置信息的字典。
        """
        return self.__dict__


class VXLANTunnel:
    """
    表示 VXLAN 隧道的配置类，用于管理 VXLAN 隧道的各项参数。
    """
    
    def __init__(self):
        """
        初始化 VXLANTunnel 类的实例，设置默认的 VXLAN 隧道参数。
        """
        self.SrcVTEPIPAddr = "192.168.1.2"  # 源 VTEP 的 IP 地址
        self.StartVniID = 10  # 起始 VNI 标识符
        self.VXLANVlanID = "1#disabled"  # VXLAN 的 VLAN ID
        self.VTEPIPNetmask = "16"  # VTEP 的 IP 网络掩码
        self.VXLANEnable = "no"  # 指示 VXLAN 隧道是否启用
        self.VlanIDStep = "1#disabled"  # VLAN ID 的步长
        self.VTEPDstMac = "68:91:d0:01:01:01#disabled"  # 目的 VTEP 的 MAC 地址
        self.StepVniID = 10  # VNI 标识符的步长
        self.VTEPIPVersion = 4  # VTEP 使用的 IP 版本，默认为 IPv4
        self.VniIdCount = 10  # VNI 标识符的数量
        self.DstVTEPIPAddr = "192.168.2.2"  # 目的 VTEP 的 IP 地址
        self.TunnelCount = 1  # 隧道数量
    
    def set_src_vtep_ip(self, ip: str):
        """
        设置源 VTEP 的 IP 地址。

        Args:
            ip (str): 要设置的源 VTEP 的 IP 地址。
        """
        self.SrcVTEPIPAddr = ip
    
    def set_dst_vtep_ip(self, ip: str):
        """
        设置目的 VTEP 的 IP 地址。

        Args:
            ip (str): 要设置的目的 VTEP 的 IP 地址。
        """
        self.DstVTEPIPAddr = ip
    
    def set_start_vni_id(self, vni: int):
        """
        设置起始 VNI 标识符。

        Args:
            vni (int): 要设置的起始 VNI 标识符。
        """
        self.StartVniID = vni
    
    def set_vxlan_vlan_id(self, vlan_id: str):
        """
        设置 VXLAN 的 VLAN ID。

        Args:
            vlan_id (str): 要设置的 VLAN ID。
        """
        self.VXLANVlanID = vlan_id
    
    def set_vtep_netmask(self, netmask: str):
        """
        设置 VTEP 的 IP 网络掩码。

        Args:
            netmask (str): 要设置的网络掩码。
        """
        self.VTEPIPNetmask = netmask
    
    def set_vxlan_enable(self, enable: bool):
        """
        设置 VXLAN 隧道的启用状态。

        Args:
            enable (bool): 若为 True，则启用 VXLAN 隧道；若为 False，则禁用。
        """
        self.VXLANEnable = "yes" if enable else "no"
    
    def set_vlan_id_step(self, step: str):
        """
        设置 VLAN ID 的步长。

        Args:
            step (str): 要设置的 VLAN ID 步长。
        """
        self.VlanIDStep = step
    
    def set_vtep_dst_mac(self, mac: str):
        """
        设置目的 VTEP 的 MAC 地址。

        Args:
            mac (str): 要设置的目的 VTEP 的 MAC 地址。
        """
        self.VTEPDstMac = mac
    
    def set_step_vni_id(self, step: int):
        """
        设置 VNI 标识符的步长。

        Args:
            step (int): 要设置的 VNI 标识符步长。
        """
        self.StepVniID = step
    
    def set_vtep_ip_version(self, version: int):
        """
        设置 VTEP 使用的 IP 版本。

        Args:
            version (int): 要设置的 IP 版本，必须为 4 或 6。

        Raises:
            ValueError: 当传入的 IP 版本不是 4 或 6 时抛出。
        """
        if version in (4, 6):
            self.VTEPIPVersion = version
        else:
            raise ValueError("Only IP version 4 or 6 is supported.")
    
    def set_vni_id_count(self, count: int):
        """
        设置 VNI 标识符的数量。

        Args:
            count (int): 要设置的 VNI 标识符数量。
        """
        self.VniIdCount = count
    
    def set_tunnel_count(self, count: int):
        """
        设置隧道数量。

        Args:
            count (int): 要设置的隧道数量。
        """
        self.TunnelCount = count
    
    def to_dict(self):
        """
        将 VXLANTunnel 实例的属性转换为字典。

        Returns:
            dict: 包含 VXLAN 隧道配置信息的字典。
        """
        return self.__dict__


class QoSConfiguration:
    """
    表示 QoS 配置的类，用于管理 QoS 相关的各项参数。
    """
    
    def __init__(self):
        """
        初始化 QoSConfiguration 类的实例，设置默认的 QoS 配置参数。
        """
        self.RoCEv2PFCMode = "no"  # RoCEv2 PFC 模式是否启用
        self.VlanPriority = "3"  # VLAN 优先级
        self.IPDscpPriority = "24"  # IP DSCP 优先级
        self.ECN = "00"  # ECN 字段值
        self.RoCEv2PFCList = "0,0,0,0,1,0,0,0"  # RoCEv2 PFC 列表
        self.PriorityEnable = "DscpBased"  # 优先级启用模式
    
    def set_roce_pfc_mode(self, enable: bool):
        """
        设置 RoCEv2 PFC 模式的启用状态。

        Args:
            enable (bool): 若为 True，则启用 RoCEv2 PFC 模式；若为 False，则禁用。
        """
        self.RoCEv2PFCMode = "yes" if enable else "no"
    
    def set_vlan_priority(self, priority: str):
        """
        设置 VLAN 优先级。

        Args:
            priority (str): 要设置的 VLAN 优先级。
        """
        self.VlanPriority = priority
    
    def set_ip_dscp_priority(self, dscp: str):
        """
        设置 IP DSCP 优先级。

        Args:
            dscp (str): 要设置的 IP DSCP 优先级。
        """
        self.IPDscpPriority = dscp
    
    def set_ecn(self, ecn: str):
        """
        设置 ECN 字段值。

        Args:
            ecn (str): 要设置的 ECN 字段值，必须是 2 位十六进制字符串。

        Raises:
            ValueError: 当传入的 ECN 字段值不是 2 位十六进制字符串时抛出。
        """
        if len(ecn) == 2 and all(c in "0123456789ABCDEFabcdef" for c in ecn):
            self.ECN = ecn.upper()
        else:
            raise ValueError("ECN must be a 2-digit hex string (e.g., '00', '01', ..., 'FF').")
    
    def set_roce_pfc_list(self, pfc_list: str):
        """
        设置 RoCEv2 PFC 列表。

        Args:
            pfc_list (str): 要设置的 RoCEv2 PFC 列表，必须是 8 个以逗号分隔的 '0' 或 '1'。

        Raises:
            ValueError: 当传入的 RoCEv2 PFC 列表不符合格式要求时抛出。
        """
        parts = pfc_list.split(",")
        if len(parts) != 8 or not all(p in ("0", "1") for p in parts):
            raise ValueError("RoCEv2PFCList must be 8 comma-separated values of '0' or '1'.")
        self.RoCEv2PFCList = pfc_list
    
    def set_priority_enable(self, mode: str):
        """
        设置优先级启用模式。

        Args:
            mode (str): 要设置的优先级启用模式，必须是 'DscpBased'、'None' 或 'VlanBased'。

        Raises:
            ValueError: 当传入的模式不是 'DscpBased'、'None' 或 'VlanBased' 时抛出。
        """
        if mode in ("DscpBased", "None", "VlanBased"):
            self.PriorityEnable = mode
        else:
            raise ValueError("PriorityEnable must be one of 'DscpBased', 'VlanBased', or 'None'.")
    
    def to_dict(self):
        """
        将 QoSConfiguration 实例的属性转换为字典。

        Returns:
            dict: 包含 QoS 配置信息的字典。
        """
        return self.__dict__


class MACSEC:
    """
    表示 MACsec 配置的类，用于管理 MACsec 相关的各项参数。
    """
    
    def __init__(self):
        """
        初始化 MACSEC 类的实例，设置默认的 MACsec 配置参数。
        """
        self.MACSECEnable = "no"  # MACsec 是否启用
        self.CAK_VALUE = "000102030405060708090a0b0c0d0e0f"  # CAK 值
        self.macsec_PN = 1  # MACsec 的 PN 值
        self.macsec_cipher_suite = "gcm-aes-128"  # MACsec 使用的加密套件
        self.CAK_NAME = "1"  # CAK 名称
        self.SCI_MAC = "001122334455"  # SCI MAC 地址
        self.PORT_Identifer = 1  # 端口标识符
    
    def set_macsec_enable(self, enable: bool):
        """
        设置 MACsec 的启用状态。

        Args:
            enable (bool): 若为 True，则启用 MACsec；若为 False，则禁用。
        """
        self.MACSECEnable = "yes" if enable else "no"
    
    def set_cak_value(self, cak: str):
        """
        设置 CAK 值。

        Args:
            cak (str): 要设置的 CAK 值，必须是 32 位十六进制字符串。

        Raises:
            ValueError: 当传入的 CAK 值不是 32 位十六进制字符串时抛出。
        """
        if len(cak) == 32 and all(c in "0123456789abcdefABCDEF" for c in cak):
            self.CAK_VALUE = cak.lower()
        else:
            raise ValueError("CAK_VALUE must be a 128-bit (32 hex chars) hex string.")
    
    def set_cak_name(self, name: str):
        """
        设置 CAK 名称。

        Args:
            name (str): 要设置的 CAK 名称。
        """
        self.CAK_NAME = name
    
    def set_cipher_suite(self, suite: str):
        """
        设置 MACsec 使用的加密套件。

        Args:
            suite (str): 要设置的加密套件，必须是 'gcm-aes-128' 或 'gcm-aes-256'。

        Raises:
            ValueError: 当传入的加密套件不支持时抛出。
        """
        if suite in ("gcm-aes-128", "gcm-aes-256"):
            self.macsec_cipher_suite = suite
        else:
            raise ValueError("Unsupported cipher suite.")
    
    def set_sci_mac(self, mac: str):
        """
        设置 SCI MAC 地址。

        Args:
            mac (str): 要设置的 SCI MAC 地址，必须是 12 位十六进制字符串。

        Raises:
            ValueError: 当传入的 SCI MAC 地址不是 12 位十六进制字符串时抛出。
        """
        if len(mac) == 12 and all(c in "0123456789abcdefABCDEF" for c in mac):
            self.SCI_MAC = mac.lower()
        else:
            raise ValueError("SCI_MAC must be a 12-character hex MAC address without separators.")
    
    def set_port_identifier(self, port: int):
        """
        设置端口标识符。

        Args:
            port (int): 要设置的端口标识符。
        """
        self.PORT_Identifer = port
    
    def set_pn(self, pn: int):
        """
        设置 MACsec 的 PN 值。

        Args:
            pn (int): 要设置的 PN 值。
        """
        self.macsec_PN = pn
    
    def to_dict(self):
        """
        将 MACSEC 实例的属性转换为字典。

        Returns:
            dict: 包含 MACsec 配置信息的字典。
        """
        return self.__dict__


class MsgFragSet:
    """
    IP报文分片设置的类，用于管理消息分片相关的各项参数。
    """
    
    def __init__(self):
        """
        初始化 MsgFragSet 类的实例，设置默认的消息分片设置参数。
        """
        self.IPv6FragEnable = "no"  # IPv6 分片是否启用
        self.IPv6UDPEnable = "no"  # IPv6 UDP 是否启用
        self.PccketFragmentDisorder = "no"  # 数据包分片乱序是否启用
        self.IPv4UDPEnable = "no"  # IPv4 UDP 是否启用
        self.PortMTU = "1500"  # 端口 MTU 值
        self.PccketFragmentHeadpkt = "no"  # 仅首发包是否启用
        self.MTUCoverEnable = "no"  # MTU 覆盖是否启用
        self.IPv6TCPMSS = "100"  # IPv6 TCP MSS 值
        self.PccketFragmentOverlap = "no"  # 数据包分片重叠是否启用
        self.IPv4FragEnable = "no"  # IPv4 分片是否启用
        self.IPv4TCPMSS = "1460"  # IPv4 TCP MSS 值
    
    def set_ipv6_frag_enable(self, enable: bool):
        """
        设置 IPv6 分片的启用状态。

        Args:
            enable (bool): 若为 True，则启用 IPv6 分片；若为 False，则禁用。
        """
        self.IPv6FragEnable = "yes" if enable else "no"
    
    def set_ipv6_udp_enable(self, enable: bool):
        """
        设置 IPv6 UDP 的启用状态。

        Args:
            enable (bool): 若为 True，则启用 IPv6 UDP；若为 False，则禁用。
        """
        self.IPv6UDPEnable = "yes" if enable else "no"
    
    def set_ipv4_frag_enable(self, enable: bool):
        """
        设置 IPv4 分片的启用状态。

        Args:
            enable (bool): 若为 True，则启用 IPv4 分片；若为 False，则禁用。
        """
        self.IPv4FragEnable = "yes" if enable else "no"
    
    def set_ipv4_udp_enable(self, enable: bool):
        """
        设置 IPv4 UDP 的启用状态。

        Args:
            enable (bool): 若为 True，则启用 IPv4 UDP；若为 False，则禁用。
        """
        self.IPv4UDPEnable = "yes" if enable else "no"
    
    def set_packet_disorder(self, enable: bool):
        """
        设置数据包分片乱序的启用状态。

        Args:
            enable (bool): 若为 True，则启用数据包分片乱序；若为 False，则禁用。
        """
        self.PccketFragmentDisorder = "yes" if enable else "no"
    
    def set_packet_headpkt(self, enable: bool):
        """
        设置仅发首包首包的启用状态。

        Args:
            enable (bool): 若为 True，则启用数据包分片首包；若为 False，则禁用。
        """
        self.PccketFragmentHeadpkt = "yes" if enable else "no"
    
    def set_packet_overlap(self, enable: bool):
        """
        设置数据包分片重叠的启用状态。

        Args:
            enable (bool): 若为 True，则启用数据包分片重叠；若为 False，则禁用。
        """
        self.PccketFragmentOverlap = "yes" if enable else "no"
    
    def set_mtu_cover_enable(self, enable: bool):
        """
        设置 MTU 覆盖的启用状态。

        Args:
            enable (bool): 若为 True，则启用 MTU 覆盖；若为 False，则禁用。
        """
        self.MTUCoverEnable = "yes" if enable else "no"
    
    def set_port_mtu(self, mtu: int):
        """
        设置端口 MTU 值。

        Args:
            mtu (int): 要设置的端口 MTU 值，必须是正整数。

        Raises:
            ValueError: 当传入的端口 MTU 值不是正整数时抛出。
        """
        if mtu > 0:
            self.PortMTU = mtu
        else:
            raise ValueError("MTU must be a positive integer.")
    
    def set_ipv4_tcp_mss(self, mss: str):
        """
        设置 IPv4 TCP MSS 值。

        Args:
            mss (str): 要设置的 IPv4 TCP MSS 值。
        """
        self.IPv4TCPMSS = mss
    
    def set_ipv6_tcp_mss(self, mss: str):
        """
        设置 IPv6 TCP MSS 值。

        Args:
            mss (str): 要设置的 IPv6 TCP MSS 值。
        """
        self.IPv6TCPMSS = mss
    
    def to_dict(self):
        """
        将 MsgFragSet 实例的属性转换为字典。

        Returns:
            dict: 包含消息分片设置信息的字典。
        """
        return self.__dict__


class Vlan:
    """
    表示 VLAN 配置的类，用于管理 VLAN 相关的各项参数。
    """
    
    def __init__(self):
        """
        初始化 Vlan 类的实例，设置默认的 VLAN 配置参数。
        """
        self.OuterVlanID = "1#disabled"  # 外层 VLAN ID
        self.QinqType = "0x88A8#disabled"  # QinQ 类型
        self.VlanID = "1#disabled"  # VLAN ID
    
    def set_outer_vlan_id(self, vlan_id: str):
        """
        设置外层 VLAN ID。

        Args:
            vlan_id (str): 要设置的外层 VLAN ID。
        """
        self.OuterVlanID = vlan_id
    
    def set_qinq_type(self, qinq: str):
        """
        设置 QinQ 类型。

        Args:
            qinq (str): 要设置的 QinQ 类型，必须是十六进制字符串并以 '0x' 开头。

        Raises:
            ValueError: 当传入的 QinQ 类型不以 '0x' 开头时抛出。
        """
        if not qinq.startswith("0x"):
            raise ValueError("QinqType should be a hex string starting with '0x'")
        self.QinqType = qinq
    
    def set_vlan_id(self, vlan_id: str):
        """
        设置 VLAN ID。

        Args:
            vlan_id (str): 要设置的 VLAN ID。
        """
        self.VlanID = vlan_id
    
    def to_dict(self):
        """
        将 Vlan 实例的属性转换为字典。

        Returns:
            dict: 包含 VLAN 配置信息的字典。
        """
        return self.__dict__


class VirtualRouterConfigDict:
    def __init__(self, enable=False, version="v4", protocol="Static", ip_addr="", mask="", next_hop="",
                 side="client"):
        self.VirtualRouterEnable = "yes" if enable else "no"
        self.SubnetNumber = "1" if version == "v4" else "2"
        self.SubnetVersion = version
        
        # 根据版本设置默认值
        if version == "v4":
            self.VirtualRouterIPAddr = ip_addr or ("17.0.0.2" if side == "client" else "17.0.0.3")
            self.VirtualRouterMask = mask or "16"
            self.VirtualRouterNextHop = next_hop or "17.0.0.1#disabled"
        else:
            self.VirtualRouterIPAddr = ip_addr or ("3ffe:0:17:0::1:2" if side == "client" else "3ffe:0:17:0::1:3")
            self.VirtualRouterMask = mask or "64"
            self.VirtualRouterNextHop = next_hop or "3ffe:0:17:0::1:1#disabled"
        
        self.VirtualRouterProtocol = protocol
    
    def set_enable(self, enable: bool):
        self.VirtualRouterEnable = "yes" if enable else "no"
    
    def set_protocol(self, protocol: str):
        self.VirtualRouterProtocol = protocol
    
    def set_ip_address(self, ip: str):
        self.VirtualRouterIPAddr = ip
    
    def set_next_hop(self, hop: str):
        self.VirtualRouterNextHop = hop
    
    def to_dict(self):
        return self.__dict__


class VirtualRouterConfig:
    """
    * 虚拟边界网关配置类
    """
    
    def __init__(self, config_list=[], side="client"):
        self.side = side
        if not config_list:
            v4_config = VirtualRouterConfigDict(version="v4", side=side)
            v6_config = VirtualRouterConfigDict(version="v6", side=side)
            config_list.append(v4_config)
            config_list.append(v6_config)
        self.config_list = config_list  # 嵌套VirtualRouterConfigDict对象列表
    
    def set_config(self, index, config_dict):
        if index < 0 or index >= len(self.config_list):
            raise IndexError("Index out of range")
        self.config_list[index] = config_dict
    
    def add_config(self, config_dict):
        self.config_list.append(config_dict)
        for index, item in enumerate(self.config_list):
            item.SubnetNumber = str(index + 1)
    
    def remove_config(self, index):
        if index < 0 or index >= len(self.config_list):
            raise IndexError("Index out of range")
        del self.config_list[index]
        for index, item in enumerate(self.config_list):
            item.SubnetNumber = str(index + 1)
    
    def get_configs(self):
        return self.config_list
    
    def to_dict(self):
        return {"VirtualRouterConfig": [config.to_dict() for config in self.config_list]}


class NetworkZone:
    """
    * 虚拟网络区域配置类
    """
    
    def __init__(self, network_zone_list=[]):
        if not network_zone_list:
            ipv4_zone = NetworkZoneDict(version="v4")
            ipv6_zone = NetworkZoneDict(version="v6")
            network_zone_list.append(ipv4_zone)
            network_zone_list.append(ipv6_zone)
        self.network_zone_list = network_zone_list  # 嵌套NetworkZoneDict对象列表
    
    def set_network_zone_dict(self, index, network_zone_dict):
        if index < 0 or index >= len(self.network_zone_list):
            raise IndexError("Index out of range")
        self.network_zone_list[index] = network_zone_dict
    
    def get_network_zone(self):
        return self.network_zone_list
    
    def to_dict(self):
        return {"NetworkZone": [network_zone_dict.to_dict() for network_zone_dict in self.network_zone_list]}


class NetworkZoneDict:
    def __init__(self, enable: bool = False, version: str = "v4", start: str = "", step: str = "", mask: str = "",
                 sim_router_ip: str = "", count: int = 0, subnet_number: str = ""):
        self.NetworkZoneEnable = "yes" if enable else "no"
        self.SubnetVersion = version
        if version == "v4":
            self.NetworkZoneStart = start or "17.1.0.0"
            self.NetworkZoneStep = step or "0.1.0.0"
            self.NetworkZoneMask = mask or "16"
            self.SimulatorRouterIPAddr = sim_router_ip or "0.0.1.2#disabled"
            self.NetworkZoneCount = count or 1
            self.SubnetNumber = subnet_number or "1"
        else:
            
            self.NetworkZoneStart = start or "3ffe:0:17:2::0"
            self.NetworkZoneStep = step or "0:0:0:1::0"
            self.NetworkZoneMask = mask or "64"
            self.SimulatorRouterIPAddr = sim_router_ip or "0:0:0:1::1:2#disabled"
            self.NetworkZoneCount = count or 1
            self.SubnetNumber = subnet_number or "2"
    
    def set_network_zone_enable(self, enable: bool):
        self.NetworkZoneEnable = "yes" if enable else "no"
    
    def set_subnet_version(self, version: str):
        if version in ("v4", "v6"):
            self.SubnetVersion = version
        else:
            raise ValueError("Subnet version must be 'v4' or 'v6'")
    
    def set_network_range(self, start: str, step: str):
        self.NetworkZoneStart = start
        self.NetworkZoneStep = step
    
    def set_network_mask(self, mask: str):
        if not mask.isdigit():
            raise ValueError("Network mask must be numeric")
        self.NetworkZoneMask = mask
    
    def set_simulator_ip(self, sim_router_ip: str):
        self.SimulatorRouterIPAddr = sim_router_ip
    
    def to_dict(self):
        return ToolsUtils.to_dict(self)


class BaseCase:
    @staticmethod
    def get_current_time():
        current_time = time.localtime()
        formatted_time = time.strftime("%Y%m%d-%H_%M_%S", current_time)
        return formatted_time
    
    def __init__(self):
        now_time = self.get_current_time()
        self.TestType = None
        self.TestMode = 'TP'
        self.DUTRole = None
        self.TestName = now_time
        self.DisplayName = now_time
        self.TestDuration = 600
        self.WorkMode = "Standalone"
        self.ImageVersion = "25.06.11"
        self.DutSystemVersion = "Supernova-Cloud 25.06.11 build4407"
        self.ReportInterval = 1
        self.ProxyMode = "Reverse"
        self.IPVersion = "v4"
        
    # 设置用例类型
    def set_test_type(self, test_type):
        self.TestType = test_type
    
    # 设置测试模式
    def set_test_mode(self, test_mode):
        self.TestMode = test_mode
    
    # 设置受测设备类型
    def set_dut_role(self, dut_role):
        self.DUTRole = dut_role
    
    # 设置测试用例名称
    def set_test_name(self, test_name):
        self.TestName = test_name
    
    # 设置测试用例测试时长
    def set_test_duration(self, test_duration):
        self.TestDuration = test_duration
    
    # 设置测试测试仪工作模式
    def set_work_mode(self, work_mode):
        self.WorkMode = work_mode
    
    def to_dict(self):
        return ToolsUtils.to_dict(self)


class HttpCps:
    class Loads:
        def __init__(self):
            # 初始化配置项
            self.UserApplyMemoryMB = 4
            self.CaseAssignMemoryGB = 2
            self.DPDKHugeMemoryPct = 70
            self.SimUser = 256
            self.HttpRequestTimeoutSecond = 10000
            self.HttpTranscationStatistics = "no"
            self.HttpPercentageLatencyStat = "no"
            self.HttpRequestHashSize = 512
            self.CookieTrafficRatio = 100
            self.SendPktStatEn = "no"
            self.HttpOverLapMode = "user"
            self.HttpThinkTimeMode = "fixed"
            self.MaxThinkTime = 37500
            self.MinThinkTime = 1
            self.ThinkTime = 37500
            self.HttpThinkTimeMaxCc = 4000000
            self.HttpNewSessionTotal = 0
            self.HttpMaxRequest = 0
            self.HttpNewConnReqNum = 0
            self.NewTcpEachRequrest = "no"
            self.HttpPipelineEn = "no"
            self.SimuserFixReq = "no"
            self.HttpRedirectNewTcpEn = "no"
            self.HttpLogTraffic = "no"
            self.OnlyRecordAbnormalResponse = "no"
            self.OnlyRecordAssertFailed = "no"
            self.HttpTrafficLogCount = 1000
            self.HttpWebURLIpStatEn = "no"
            self.HttpWebStatIPNum = 10
        
        # Setter methods for each configuration item
        def set_user_apply_memory_mb(self, value):
            self.UserApplyMemoryMB = value
        
        def set_case_assign_memory_gb(self, value):
            self.CaseAssignMemoryGB = value
        
        def set_dpdk_huge_memory_pct(self, value):
            self.DPDKHugeMemoryPct = value
        
        def set_sim_user(self, value):
            self.SimUser = value
        
        def set_http_request_timeout_second(self, value):
            self.HttpRequestTimeoutSecond = value
        
        def set_http_transcation_statistics(self, value):
            self.HttpTranscationStatistics = value
        
        def set_http_percentage_latency_stat(self, value):
            self.HttpPercentageLatencyStat = value
        
        def set_http_request_hash_size(self, value):
            self.HttpRequestHashSize = value
        
        def set_cookie_traffic_ratio(self, value):
            self.CookieTrafficRatio = value
        
        def set_send_pkt_stat_en(self, value):
            self.SendPktStatEn = value
        
        def set_http_over_lap_mode(self, value):
            self.HttpOverLapMode = value
        
        def set_http_think_time_mode(self, value):
            self.HttpThinkTimeMode = value
        
        def set_max_think_time(self, value):
            self.MaxThinkTime = value
        
        def set_min_think_time(self, value):
            self.MinThinkTime = value
        
        def set_think_time(self, value):
            self.ThinkTime = value
        
        def set_http_think_time_max_cc(self, value):
            self.HttpThinkTimeMaxCc = value
        
        def set_http_new_session_total(self, value):
            self.HttpNewSessionTotal = value
        
        def set_http_max_request(self, value):
            self.HttpMaxRequest = value
        
        def set_http_new_conn_req_num(self, value):
            self.HttpNewConnReqNum = value
        
        def set_new_tcp_each_requrest(self, value):
            self.NewTcpEachRequrest = value
        
        def set_http_pipeline_en(self, value):
            self.HttpPipelineEn = value
        
        def set_simuser_fix_req(self, value):
            self.SimuserFixReq = value
        
        def set_http_redirect_new_tcp_en(self, value):
            self.HttpRedirectNewTcpEn = value
        
        def set_http_log_traffic(self, value):
            self.HttpLogTraffic = value
        
        def set_only_record_abnormal_response(self, value):
            self.OnlyRecordAbnormalResponse = value
        
        def set_only_record_assert_failed(self, value):
            self.OnlyRecordAssertFailed = value
        
        def set_http_traffic_log_count(self, value):
            self.HttpTrafficLogCount = value
        
        def set_http_web_url_ip_stat_en(self, value):
            self.HttpWebURLIpStatEn = value
        
        def set_http_web_stat_ip_num(self, value):
            self.HttpWebStatIPNum = value
        
        def to_dict(self):
            """将对象属性转换为字典格式"""
            return self.__dict__
        
    class CaseObject:
        def __init__(self):
            self.Variate = '无'
            self.Monitor = '默认监控器对象Ping'
            self.WebTestProjectName = '默认网络设备测试项目'
            self.WebTestProjectId = '6736b97647d27cb2a9b4816a'
            self.FileObject = '默认156字节网页请求'
            self.FileObjMapFolder = '6736b97647d27cb2a9b4819f'
        
        def set_variate(self, variate):
            self.Variate = variate
        
        def set_monitor(self, monitor):
            self.Monitor = monitor
        
        def set_web_test_project_name(self, web_test_project_name):
            self.WebTestProjectName = web_test_project_name
        
        def set_web_test_project_id(self, web_test_project_id):
            self.WebTestProjectId = web_test_project_id
        
        def set_file_object(self, file_object):
            self.FileObject = file_object
        
        def set_file_obj_map_folder(self, file_obj_map_folder):
            self.FileObjMapFolder = file_obj_map_folder
        
        def to_dict(self):
            """将对象属性转换为字典格式"""
            return self.__dict__
    
    class ClientProfiles:
        def __init__(self):
            self.SourcePortRange = "10000-65535"
            self.Actions = {}
            self.RequestHeader = [
                "User-Agent: Firefox/41.0"
            ]
            self.ClientCloseMode = "Reset"

        def set_source_port_range(self, SourcePortRange):
            self.SourcePortRange = SourcePortRange
        
        def to_dict(self):
            return self.__dict__
    
    class ServerProfiles:
        def __init__(self):
            self.ServerPort = "80"

            self.ServerCloseMode = "3Way_Fin"
            self.ResponseHeader = [
                "Server: nginx/1.9.5",
                "Content-Type: text/html"
            ]


            self.ServerRecvRqtTimeOut = 300000
            # self.Http1CloseDelayms = 0
            self.Http1CloseDelayms = 500

        def set_server_port(self, ServerPort):
            self.ServerPort = ServerPort
        
        def set_server_recvrqt_timeout(self, ServerRecvRqtTimeOut):
            self.ServerRecvRqtTimeOut = ServerRecvRqtTimeOut
        
        def set_http1_close_delayms(self, Http1CloseDelayms):
            self.Http1CloseDelayms = Http1CloseDelayms
        
        def to_dict(self):
            return self.__dict__
    
    def __init__(self):
        self.Loads = HttpCps.Loads()
        self.CaseObject = HttpCps.CaseObject()
        self.ClientProfiles = HttpCps.ClientProfiles()
        self.ServerProfiles = HttpCps.ServerProfiles()
    
    def to_dict(self):
        return {
            "Loads": self.Loads.to_dict(),
            "CaseObject": self.CaseObject.to_dict(),
            "ClientProfiles": self.ClientProfiles.to_dict(),
            "ServerProfiles": self.ServerProfiles.to_dict()
        }


class PortConfig:
    def __init__(self, dut_role, port_name, port_side):
        if port_side == "client":
            self.NetworkSubnets = [BaseSubnet.create_subnet(dut_role)[0].to_dict()]
        elif port_side == "server":
            self.NetworkSubnets = [BaseSubnet.create_subnet(dut_role)[1].to_dict()]
        
        self.VirtualRouterConfig = VirtualRouterConfig().to_dict().get("VirtualRouterConfig")
        # 虚拟网络区域
        self.NetworkZone = NetworkZone().to_dict().get("NetworkZone")
        # 限速
        self.PortSpeedLimit = [PortSpeedLimit().to_dict()]
        self.SimUserSpeedLimit = [SimUserSpeedLimit().to_dict()]
        # 抓包过滤
        self.PacketCapture = [PacketCapture().to_dict()]
        self.PacketFilter = [PacketFilter().to_dict()]
        # VXLAN封装
        self.VXLANTunnel = VXLANTunnel().to_dict()
        self.GTPUTunnel = GTPUTunnel().to_dict()
        self.MsgFragSet = MsgFragSet().to_dict()
        self.MACSEC = MACSEC().to_dict()
        self.QoSConfiguration = QoSConfiguration().to_dict()
        
        # 散装字段
        self.Interface = port_name
        print("___________2040")
        print(self.Interface)
        self.PortEnable = "yes"
        self.PortSide = port_side
        self.PortSpeedDetectMode = "Autoneg"
        self.MacMasquerade = "A2:01#disabled"
        self.TesterPortMacAddress = "68:91:d0:66:b1:b6#disabled"
        self.NextPortMacMethod = "ARP_NSNA#disabled"
        self.PortRXRSS = "no"
        self.HeadChecksumConf = {
            "IPV4HeadChecksumType": "auto",
            "TCPHeadChecksumType": "auto",
            "UDPHeadChecksumType": "auto"
        }
        self.nb_txd = 4096
        self.nb_rxd = 4096
        self.nictype = "PERF"
        self.device = "NetiTest IT2X010GF47LA 1G/10G SmartNIC"
        self.sendqueue = "4"
        self.receivequeue = "4"
        self.CoreBind = "2"
        self.OuterVlanID = "1#disabled"
        self.QinqType = "0x88A8#disabled"
        self.VlanID = "1#disabled"
    
    def set_port_core_bind(self, core_bind):
        self.CoreBind = core_bind
        
    def to_dict(self):
        # return ToolsUtils.to_dict(self)
        return self.__dict__


class HttpClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.token = None
    
    def login(self, payload):
        url = f"{self.base_url}/api/user/login"
        print(f"Login URL: {url}")
        response = self.session.post(url, json=payload)
        if response.status_code == 200:
            print("Login successful.")
            self.user = payload["name"]
            self.token = response.json().get("token")
        else:
            raise Exception(f"Login failed: {response.status_code} - {response.text}")

    def get(self, path, params=None):
        url = f"{self.base_url}{path}"
        print(url)
        headers = self._build_headers()
        response = self.session.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code}, {response.text}")
        print(response.json())
        return response.json()

    def post(self, path, data=None):
        url = f"{self.base_url}{path}"
        headers = self._build_headers()
        response = self.session.post(url, headers=headers, json=data)
        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code}, {response.text}")
        return response.json()
    
    def _build_headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers


class TestCaseBuilder:
    def __init__(self, host, test_type, dut_role):
        self.host = host
        self.test_type = test_type
        self.dut_role = dut_role
        self.case_model = TestFactory.create(test_type)
    
    def build(self):
        base = BaseCase()
        base.set_dut_role(self.dut_role)
        base.set_test_type(self.test_type)
        data = base.to_dict()
        data["Specifics"] = self._build_specifics()
        data["NetworkConfig"] = self._build_network_config()
        return data
    
    def _build_specifics(self):
        specifics = {"TestType": self.test_type}
        for field in ["Loads", "CaseObject", "ClientProfiles", "ServerProfiles"]:
            obj = getattr(self.case_model, field)
            specifics[field] = obj.to_dict()
        return [specifics]
    
    def _build_network_config(self):
        return {
            "NetworkControl": NetworkControlConfig().to_dict(),
            "SlaveHost": [{"Host": self.host, "Ports": []}]
        }


class TestCase:
    def __init__(self, host, http_client, test_type, dut_role):
        self.report_id = None
        self.test_type = test_type
        self.host = host
        self.client = http_client
        self.case_id = None
        self.case_config = TestCaseBuilder(self.host, test_type, dut_role).build()
        self.port_list = []
        self.get_default_values()
        
    @staticmethod
    def parse_port_list(port_str):
        return port_str.split(',') if port_str else []

    def check_cpu_cores_is_valid(self):
        """
        * 校验cpu核心绑定是否合法
        :return:
        """
        pass

    def get_default_values(self):
        """
        * 从测试仪获取并替换默认值
        """
        # 获取infos
        infos_ret = self.client.get("/api/system/infos")
        if infos_ret.get("ErrorCode") == 0:
            infos_dict = infos_ret["Data"]
            self.case_config["WorkMode"] = infos_dict["WorkMode"]["workMode"]
            self.case_config["DutSystemVersion"] = infos_dict["Version"]
            self.case_config["ImageVersion"] = infos_dict["Version"].split()[1]
            for mem in infos_dict["MemoryMgmt"]["Used"]:

                if mem["ResourceUser"] == self.client.user:
                    self.case_config["Specifics"][0]["Loads"]["CaseAssignMemoryGB"] = mem["ResourceOccupy"]
                    self.case_config["Specifics"][0]["Loads"]["UserApplyMemoryMB"] = mem["ResourceOccupy"]

        dpdk_hyge_memory_pct = self.client.get("/api/case/DpdkHugeMemoryPct", {"testType": self.test_type})
        # 大页内存占比
        self.case_config["Specifics"][0]["Loads"]["DPDKHugeMemoryPct"] = dpdk_hyge_memory_pct.get("Data", {}).get("def",
                                                                                                                  70)

        if self.test_type in ["HttpCc", "HttpsCc"]:
            cc_cfg = self.client.get("/api/case/conn/cfg", {"testType": self.test_type})
            # 并发连接数
            self.case_config["Specifics"][0]["Loads"]["ConcurrentConnection"] = cc_cfg.get("Data", {}).get("def",
                                                                                                           1296000)

    def update_port_default_values(self):
        """
        * 更新端口默认值
        """
        port_info_ret = self.client.get(f"/api/system/ports/show")
        if port_info_ret.get("ErrorCode") == 0:
            nic_infos_ret = self.client.get(f"/api/system/netnic/infos")

            for port in self.port_list:
                port_name = port.Interface
                nic_infos_list = nic_infos_ret["Data"]["PortArray"]
                for nic_info in nic_infos_list:
                    if nic_info["name"] == port_name:
                        port.device = nic_info["name_info"]["device"]
                        port.driver = nic_info["name_info"]["driver"]
                        port.sendqueue = nic_info["name_info"]["combined"]
                        port.receivequeue = nic_info["name_info"]["combined"]
                        port.nictype = nic_info["name_info"]["nictype"]

                traffic_port_list = port_info_ret["Data"]["TrafficPorts"]
                for traffic_port in traffic_port_list:
                    if traffic_port["name"] == port_name:
                        if self.test_type.startswith("RFC"):
                            port.CoreBind = traffic_port["rfc_cores"]
                        else:
                            port.CoreBind = traffic_port["port_cores"]

                tx_rx_dict = self.client.get(f"/api/ports/driver", {"Driver": port.driver, "Type": self.test_type})
                tx_rx_info = tx_rx_dict["Data"]
                port.nb_txd = tx_rx_info["nb_txd"]
                port.nb_rxd = tx_rx_info["nb_rxd"]
    
    def Getresult(self):
        payload = {
            "ReportID": self.report_id,
            "TestType": self.test_type,
            "TestID": self.case_id,
            "Layer": "layer2",
            "LayerTabs": ["sum"]
        }
        res = self.client.post("/api/running/get/layer2", payload)
        if res.get("ErrorCode") == 0:
            print(res.get("Data"))
        else:
            print("get layer2 error", res)
    
    def Monitor(self):
        while True:
            time.sleep(1)
            data = self.client.get("/api/running/status")

            if data["ErrorCode"] == 0:
                if "TestStatus" in data and data["TestStatus"] == "Running":
                    self.report_id = data.get("Data")['ReportID']
                    break
    
    def Apply(self, case_config):
        res = self.client.post("/api/case", case_config)
        if res.get("ErrorCode") == 0:
            self.case_id = res.get("Data")
            print('Use case created successfully', res)
        else:
            print("Use case creation failed")
        time.sleep(1)
    
    def Start(self):
        res = self.client.get(f"/api/case/{self.case_id}/start")

        if res.get("ErrorCode") == 0:
            print("Test case startup successful")
        else:
            print("Test case startup failed", res)
    
    def Config(self, key, *args):
        
        if key == "Interface":
            dut_role = self.case_config.get("DUTRole")
            if dut_role == "Gateway":
                client_port_list = self.parse_port_list(args[0])
                server_port_list = self.parse_port_list(args[1])
                port_subnet_list = []
                for port_name in client_port_list:
                    port_config = PortConfig(dut_role, port_name, 'client')
                    self.port_list.append(port_config)
                    port_subnet_list.append(port_config.to_dict())
                
                for port_name in server_port_list:
                    port_config = PortConfig(dut_role, port_name, 'server')
                    self.port_list.append(port_config)
                    port_subnet_list.append(port_config.to_dict())
                self.case_config["NetworkConfig"]["SlaveHost"][0]["Ports"] = port_subnet_list
            # 获取端口默认字段
            self.update_port_default_values()


        elif key == "InterfaceCPU":
            # self.check_cpu_cores_is_valid()
            for port_core_str in args:
                port_name = port_core_str.split(':')[0]
                core_list_str = port_core_str.split(':')[1].strip()
                for port in self.port_list:
                    if port.Interface == port_name:
                        port.set_port_core_bind(core_list_str)

        elif key == "NetworkSubnet":
            for arg in args:
                if type(arg) is dict:
                    for key, val_dict in arg.items():
                        port_name = key
                        for port_config in self.case_config["NetworkConfig"]["SlaveHost"][0]["Ports"]:
                            if port_config["Interface"] == port_name:
                                port_side = port_config["PortSide"]
                                if "SubnetNumber" not in val_dict:
                                    raise ValueError("The 'SubnetNumber' parameter is missing")
                                network_subnets = port_config["NetworkSubnets"]
                                for network_subnet in network_subnets:
                                    val_dict["SubnetNumber"] = str(val_dict["SubnetNumber"])
                                    if network_subnet["SubnetNumber"] == val_dict["SubnetNumber"]:
                                        # 修改主机子网
                                        if "IpAddrRange" in val_dict:
                                            ip_obj = ipaddress.ip_address(val_dict["IpAddrRange"])
                                            if ip_obj.version == 4:
                                                val_dict["SubnetVersion"] = "v4"
                                            else:
                                                val_dict["SubnetVersion"] = "v6"
                                        network_subnet.update(val_dict)
                                        break
                                else:
                                    # 添加主机子网
                                    if "IpAddrRange" not in val_dict:
                                        raise ValueError(
                                            "If you want to add a subnet, specify 'IpAddrRange' parameters")
                                    if self.case_config.get("DUTRole") == "Gateway":
                                        if port_side == "client":
                                            # 添加客户端子网
                                            if "ServerIPRange" not in val_dict and "SubnetServicePort" not in val_dict:
                                                raise ValueError(
                                                    "If you want to add a subnet for the client role, specify the server IP address or server port")
                                            if "SubnetServicePort" in val_dict and "PeerServerSubnet" not in val_dict:
                                                raise ValueError(
                                                    "If the parameter 'SubnetServicePort' is specified, the parameter 'PeerServerSubnet' must be specified")
                                            if "ServerIPRange" in val_dict:
                                                val_dict["ServerAddressFormat"] = "IP"
                                            elif "SubnetServicePort" in val_dict:
                                                val_dict["ServerAddressFormat"] = "Port"
                                            
                                            ip_obj = ipaddress.ip_address(val_dict["IpAddrRange"])
                                            if ip_obj.version == 4:
                                                val_dict["SubnetVersion"] = "v4"
                                                new_subnet_dict = BaseSubnet.create_subnet("Gateway", version=4)[
                                                    0].to_dict()
                                            else:
                                                val_dict["SubnetVersion"] = "v6"
                                                new_subnet_dict = BaseSubnet.create_subnet("Gateway", version=6)[
                                                    0].to_dict()
                                            new_subnet_dict.update(val_dict)
                                            port_config["NetworkSubnets"].append(new_subnet_dict)
                                        else:
                                            # 添加服务端子网
                                            ip_obj = ipaddress.ip_address(val_dict["IpAddrRange"])
                                            if ip_obj.version == 4:
                                                val_dict["SubnetVersion"] = "v4"
                                                new_subnet_dict = BaseSubnet.create_subnet("Gateway", version=4)[
                                                    1].to_dict()
                                            else:
                                                val_dict["SubnetVersion"] = "v6"
                                                new_subnet_dict = BaseSubnet.create_subnet("Gateway", version=6)[
                                                    1].to_dict()
                                            new_subnet_dict.update(val_dict)
                                            port_config["NetworkSubnets"].append(new_subnet_dict)


class TestFactory:
    @staticmethod
    def create(test_type):
        if test_type == "HttpCps":
            return HttpCps()
        elif test_type == "HttpForceCps":
            return HttpCps()
        elif test_type == "HttpCc":
            return HttpCps()
        elif test_type == "HttpThroughput":
            return HttpCps()
        else:
            raise ValueError(f"未知测试类型：{test_type}")


class CreateProject:
    def __init__(self):
        self.host = ''
        self.host_port = 80
        self.client = None
    
    def is_accessible(self):
        if not NetworkUtils.ping_host(self.host):
            print(f"Host {self.host} network unreachable")
            return False
        if not NetworkUtils.check_port(self.host, self.host_port):
            print(f"Port {self.host_port} unreachable")
            return False
        return True
    
    def Connect(self, host, port):
        self.host = host
        self.host_port = port
        
        if not self.is_accessible():
            return None
        
        base_url = f"http://{self.host}:{self.host_port}"
        self.client = HttpClient(base_url)
        print(f"Connected to {self.client.base_url}")
    
    def Login(self, username, password):
        if not self.is_accessible():
            return None
        
        payload = {
            "name": username,
            "password": password
        }
        self.client.login(payload)

        # try:
        #     response = self.client.post("/api/user/login", data=payload)
        #     if response.status_code == 200:
        #         print("Login successful")
        #         self.client.user = username
        #         return response.json()
        #     else:
        #         print(f"Login failed, status code: {response.status_code}")
        #         return None
        # except Exception as e:
        #     print(f"Request exception: {e}")
        #     return None
    
    def CreateCase(self, test_type, dut_role):
        test_case = TestCase(self.host, self.client, test_type, dut_role)
        return test_case
