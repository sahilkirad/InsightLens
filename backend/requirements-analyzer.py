#!/usr/bin/env python3
"""
Python Version Compatibility Analyzer
Analyzes your requirements and determines the optimal Python version for deployment.
"""

import subprocess
import sys
import json
from typing import Dict, List, Tuple

class PythonVersionAnalyzer:
    def __init__(self):
        self.requirements_file = "requirements-render.txt"
        self.compatibility_matrix = {
            "fastapi": {
                "0.104.1": {"python": ">=3.8", "pydantic": ">=2.0.0"},
                "0.95.2": {"python": ">=3.7", "pydantic": ">=1.7.4,<3.0.0"}
            },
            "pydantic": {
                "2.5.0": {"python": ">=3.7", "requires_rust": True},
                "1.10.13": {"python": ">=3.6", "requires_rust": False}
            },
            "uvicorn": {
                "0.24.0": {"python": ">=3.8"},
                "0.22.0": {"python": ">=3.7"}
            },
            "firebase-admin": {
                "6.2.0": {"python": ">=3.7"}
            },
            "python-jose": {
                "3.3.0": {"python": ">=3.6"}
            },
            "passlib": {
                "1.7.4": {"python": ">=3.6"}
            },
            "bcrypt": {
                "4.0.1": {"python": ">=3.6"}
            }
        }
    
    def parse_requirements(self) -> List[Tuple[str, str]]:
        """Parse requirements file and extract package versions"""
        packages = []
        try:
            with open(self.requirements_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '==' in line:
                        package, version = line.split('==')
                        packages.append((package.strip(), version.strip()))
        except FileNotFoundError:
            print(f"❌ {self.requirements_file} not found!")
            return []
        
        return packages
    
    def analyze_compatibility(self, packages: List[Tuple[str, str]]) -> Dict:
        """Analyze compatibility and recommend Python version"""
        analysis = {
            "packages": [],
            "python_versions": set(),
            "rust_required": False,
            "recommendations": [],
            "issues": []
        }
        
        for package, version in packages:
            package_info = {
                "name": package,
                "version": version,
                "compatibility": "unknown"
            }
            
            if package in self.compatibility_matrix:
                if version in self.compatibility_matrix[package]:
                    compat = self.compatibility_matrix[package][version]
                    package_info["compatibility"] = compat
                    
                    # Check if Rust compilation is required
                    if compat.get("requires_rust", False):
                        analysis["rust_required"] = True
                        analysis["issues"].append(f"⚠️ {package} {version} requires Rust compilation")
                    
                    # Add Python version requirement
                    if "python" in compat:
                        analysis["python_versions"].add(compat["python"])
                else:
                    analysis["issues"].append(f"⚠️ Unknown version {version} for {package}")
            else:
                analysis["issues"].append(f"⚠️ No compatibility data for {package}")
            
            analysis["packages"].append(package_info)
        
        # Generate recommendations
        self._generate_recommendations(analysis)
        
        return analysis
    
    def _generate_recommendations(self, analysis: Dict):
        """Generate deployment recommendations"""
        recommendations = []
        
        # Check for Rust compilation issues
        if analysis["rust_required"]:
            recommendations.append({
                "type": "warning",
                "message": "Some packages require Rust compilation",
                "solution": "Use --only-binary=all flag in build command"
            })
        
        # Recommend Python version
        if analysis["python_versions"]:
            # Find the highest minimum Python version
            min_versions = []
            for version_req in analysis["python_versions"]:
                if version_req.startswith(">="):
                    min_versions.append(version_req[2:])
            
            if min_versions:
                # Recommend a stable version
                recommended_versions = ["3.11.7", "3.11.5", "3.11.4", "3.10.12", "3.9.18"]
                
                for version in recommended_versions:
                    major, minor, patch = map(int, version.split('.'))
                    if f"{major}.{minor}" >= max(min_versions):
                        recommendations.append({
                            "type": "success",
                            "message": f"Recommended Python version: {version}",
                            "solution": f"Use python-{version} in runtime.txt"
                        })
                        break
        
        # Add general recommendations
        recommendations.append({
            "type": "info",
            "message": "Use pre-built wheels when possible",
            "solution": "Build command: pip install --only-binary=all -r requirements-render.txt"
        })
        
        analysis["recommendations"] = recommendations
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate a formatted report"""
        report = []
        report.append("=" * 60)
        report.append("🐍 PYTHON VERSION COMPATIBILITY ANALYSIS")
        report.append("=" * 60)
        report.append("")
        
        # Package Analysis
        report.append("📦 PACKAGE ANALYSIS:")
        report.append("-" * 30)
        for package in analysis["packages"]:
            status = "✅" if package["compatibility"] != "unknown" else "❓"
            report.append(f"{status} {package['name']} {package['version']}")
        report.append("")
        
        # Issues
        if analysis["issues"]:
            report.append("⚠️ ISSUES FOUND:")
            report.append("-" * 30)
            for issue in analysis["issues"]:
                report.append(f"  {issue}")
            report.append("")
        
        # Recommendations
        report.append("💡 RECOMMENDATIONS:")
        report.append("-" * 30)
        for rec in analysis["recommendations"]:
            icon = {"success": "✅", "warning": "⚠️", "info": "ℹ️"}[rec["type"]]
            report.append(f"{icon} {rec['message']}")
            report.append(f"   Solution: {rec['solution']}")
            report.append("")
        
        # Deployment Configuration
        report.append("🚀 DEPLOYMENT CONFIGURATION:")
        report.append("-" * 30)
        report.append("Build Command: pip install --only-binary=all -r requirements-render.txt")
        report.append("Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT")
        report.append("Root Directory: backend")
        report.append("")
        
        return "\n".join(report)
    
    def create_runtime_txt(self, python_version: str):
        """Create runtime.txt with recommended Python version"""
        content = f"python-{python_version}\n"
        with open("runtime.txt", "w") as f:
            f.write(content)
        print(f"✅ Created runtime.txt with Python {python_version}")
    
    def run_analysis(self):
        """Run the complete analysis"""
        print("🔍 Analyzing Python version compatibility...")
        print("")
        
        # Parse requirements
        packages = self.parse_requirements()
        if not packages:
            print("❌ No packages found to analyze!")
            return
        
        # Analyze compatibility
        analysis = self.analyze_compatibility(packages)
        
        # Generate and display report
        report = self.generate_report(analysis)
        print(report)
        
        # Create runtime.txt if recommended
        for rec in analysis["recommendations"]:
            if rec["type"] == "success" and "Recommended Python version:" in rec["message"]:
                version = rec["message"].split(": ")[1]
                self.create_runtime_txt(version)
                break

def main():
    analyzer = PythonVersionAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()
